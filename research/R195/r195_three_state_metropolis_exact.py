"""R195: finite-state Metropolis-Hastings and exact effective sample size.

Four artificial targets, two neighbor proposal rates, three starts,
24 worlds x 129 steps x 3 states = 9288 exact rational cells.
ESS of the stationary 64-state indicator mean is computed independently by
lag covariances and by dynamic propagation of additive occupancy moments.
96 fixed-seed chains are a numerical illustration, NOT convergence proofs.
"""
from __future__ import annotations
import csv,json,random,sys,unittest,zipfile
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path

HERE=Path(__file__).resolve().parent
PROTOCOL=HERE.parent.parent/"protocols/R195_MCMC_24_WORLDS_9288_EXACT_CELLS_PRESCORE_FREEZE_2026-10-21.md"
RESULT=HERE/"R195_EXACT_RESULTS.json"
EXACT=HERE/"R195_ALL_9288_EXACT_DISTRIBUTION_CELLS.csv"
KERNELS=HERE/"R195_ALL_8_EXACT_MCMC_KERNELS_AND_ESS.json"
SAMPLES=HERE/"R195_ALL_96_SEEDED_MCMC_REPLICATES.csv"
ACCEPT=HERE/"R195_FINAL_MACHINE_ACCEPTANCE.json"
ZIP=HERE/"R195_24_Exact_ThreeState_MCMC_Worlds.zip"
TARGETS=(("UNIFORM",(1,1,1)),("CENTER",(1,4,1)),("BIMODAL",(4,1,4)),("SKEW",(1,2,4)))
QS=(F(1,8),F(1,4))
STARTS=(0,1,2)
CHECKPOINTS=(0,1,2,4,8,16,32,64,128)
HORIZON=128
N=64
BURN=64
DRAWS=2048
REPLICAS=4

def check(w,q):
    if w not in [p for name,p in TARGETS] or q not in QS:
        raise ValueError("Unregistered artificial target or proposal")

def pi_of(w):
    if w not in [p for name,p in TARGETS]:
        raise ValueError("Unknown target")
    return tuple(F(x,sum(w)) for x in w)

def Q_of(q):
    if q not in QS:raise ValueError("Unknown q")
    return tuple(tuple(
        q if abs(i-j)==1 else
        (1-(1 if i in (0,2) else 2)*q if i==j else F(0))
        for j in range(3)) for i in range(3))

def kernel_A(w,q):
    check(w,q)
    Q=Q_of(q)
    rows=[]
    for i in range(3):
        row=[F(0)]*3
        row[i]=Q[i][i]
        for j in range(3):
            if i==j:continue
            a=min(F(1),F(w[j],w[i]))
            row[j]=Q[i][j]*a
            row[i]+=Q[i][j]*(1-a)
        rows.append(tuple(row))
    return tuple(rows)

def kernel_B(w,q):
    check(w,q)
    T=[[F(0)]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            if abs(i-j)==1:
                T[i][j]=q*F(min(w[i],w[j]),w[i])
        T[i][i]=1-sum(T[i],F(0))
    return tuple(tuple(r) for r in T)

def delta(s):
    if s not in STARTS:raise ValueError("Invalid initial state")
    return tuple(F(s==i) for i in range(3))

def step(v,T):
    return tuple(sum((v[i]*T[i][j] for i in range(3)),F(0)) for j in range(3))

def mm(A,B):
    return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(3)),F(0)) for j in range(3)) for i in range(3))

def mpow(T,n):
    if n<0 or n>HORIZON:raise ValueError("Unregistered power")
    ans=tuple(delta(i) for i in range(3))
    b=T
    while n:
        if n&1:ans=mm(ans,b)
        b=mm(b,b)
        n//=2
    return ans

def validate(w,q,T):
    if T!=kernel_B(w,q):raise AssertionError("MH and conductance kernels disagree")
    pi=pi_of(w)
    for i in range(3):
        if sum(T[i],F(0))!=1 or T[i][i]<=0 or any(v<0 for v in T[i]):
            raise AssertionError("Kernel not stochastic or aperiodic")
        if step(pi,T)[i]!=pi[i]:raise AssertionError("Not stationary")
        for j in range(3):
            if pi[i]*T[i][j]!=pi[j]*T[j][i]:
                raise AssertionError("Detailed balance fails")
            if abs(i-j)==1 and T[i][j]<=0:
                raise AssertionError("Irreducible path disconnected")

def tv(p,pi):
    return sum((abs(x-y) for x,y in zip(p,pi)),F(0))/2

def evolution(T,pi,start):
    v=delta(start)
    output=[]
    for t in range(HORIZON+1):
        if t in CHECKPOINTS and v!=mpow(T,t)[start]:
            raise AssertionError("Iteration and exponentiation differ")
        if sum(v,F(0))!=1 or any(x<0 for x in v):
            raise AssertionError("Out-of-simplex evolution")
        output.append((t,v,tv(v,pi)))
        if t<HORIZON:v=step(v,T)
    if any(output[t+1][2]>output[t][2] for t in range(HORIZON)):
        raise AssertionError("TV increased")
    return output

def ess_covariance(T,pi):
    p=pi[2]
    v=p*(1-p)
    if v<=0:raise AssertionError("Indicator degenerate")
    row=delta(2)
    rhos=[]
    for lag in range(1,N):
        row=step(row,T)
        rhos.append((p*row[2]-p*p)/v)
    scale=F(1)+2*sum(((1-F(k,N))*r for k,r in enumerate(rhos,1)),F(0))
    sample_variance=(v/N)*scale
    if sample_variance<=0:raise AssertionError("Nonpositive variance")
    return sample_variance,v/sample_variance,rhos,scale

def ess_additive_DP(T,pi):
    """Independent second-moment propagation for visits to state 2."""
    mass=pi
    first=tuple(pi[i]*int(i==2) for i in range(3))
    second=first
    for _ in range(1,N):
        nm=[F(0)]*3;nf=[F(0)]*3;ns=[F(0)]*3
        for i,j in product(range(3),repeat=2):
            p=T[i][j]
            x=int(j==2)
            nm[j]+=p*mass[i]
            nf[j]+=p*(first[i]+x*mass[i])
            ns[j]+=p*(second[i]+2*x*first[i]+x*mass[i])
        mass,first,second=tuple(nm),tuple(nf),tuple(ns)
    f=sum(first,F(0))
    if sum(mass,F(0))!=1 or f!=N*pi[2]:
        raise AssertionError("Occupancy DP first moment wrong")
    return (sum(second,F(0))-f*f)/(N*N)

def simulate(T,start,seed):
    rng=random.Random(seed)
    s=start
    counts=[0]*3
    for t in range(BURN+DRAWS):
        u=rng.random()
        cumulative=0.0
        after=2
        for j in range(3):
            cumulative+=float(T[s][j])
            if u<cumulative:
                after=j
                break
        s=after
        if t>=BURN:counts[s]+=1
    if sum(counts)!=DRAWS:raise AssertionError("Simulation length wrong")
    return tuple(counts),s

def file_csv(path,rows):
    with path.open("w",newline="",encoding="utf-8") as file:
        w=csv.DictWriter(file,fieldnames=list(rows[0]),lineterminator="\n")
        w.writeheader();w.writerows(rows)

def file_json(path,obj):
    path.write_text(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def run():
    exact_rows=[];replicas=[];kernel_rows=[];world_rows=[]
    for wi,(name,w) in enumerate(TARGETS):
        pi=pi_of(w)
        for qi,q in enumerate(QS):
            T=kernel_A(w,q)
            validate(w,q,T)
            variance,ess,rhos,inflate=ess_covariance(T,pi)
            if variance!=ess_additive_DP(T,pi):
                raise AssertionError("Two independent finite ESS derivations differ")
            kernel_rows.append({
                "target":name,"unnormalized_weights":list(w),"proposal_edge_probability_q":str(q),
                "target_exact_pi":[str(p) for p in pi],
                "transition_exact_matrix":[[str(x) for x in row] for row in T],
                "stationary_state2_mean_exact":str(pi[2]),
                "stationary_state2_variance_exact":str(pi[2]*(1-pi[2])),
                "stationary_lag1_to_lag63_exact_rho":[str(x) for x in rhos],
                "stationary_N64_sample_mean_variance_exact":str(variance),
                "stationary_N64_variance_inflation_exact":str(inflate),
                "stationary_N64_indicator_ESS_exact":str(ess),
                "stationary_N64_indicator_ESS_float":float(ess),
                "independent_covariance_and_occupancy_moment_DP_match":True,
            })
            for start in STARTS:
                curve=evolution(T,pi,start)
                snapshots={str(t):str(curve[t][2]) for t in CHECKPOINTS}
                boundary={}
                for key,eps in (("TV_at_most_1_over_20",F(1,20)),
                                ("TV_at_most_1_over_100",F(1,100))):
                    found=next((t for t,x,v in curve if v<=eps),None)
                    boundary[key]=found if found is not None else "NOT_REACHED_BY_128"
                world_rows.append({
                    "target":name,"q":str(q),"start_state":start,
                    "TV_start_exact":str(curve[0][2]),"TV_t128_exact":str(curve[-1][2]),
                    "snapshot_TV_exact":snapshots,**boundary,
                    "full_129_times_and_9_independent_power_checks_pass":True
                })
                for t,p,dist in curve:
                    for state in range(3):
                        exact_rows.append({
                            "target":name,"q":str(q),"start_state":start,
                            "step_t":t,"observed_state":state,
                            "exact_probability":str(p[state]),"exact_total_variation":str(dist)
                        })
                for replica in range(REPLICAS):
                    seed=195000+wi*10000+qi*1000+start*100+replica
                    count,end=simulate(T,start,seed)
                    empirical=F(count[2],DRAWS)
                    replicas.append({
                        "target":name,"q":str(q),"start_state":start,"replicate":replica,
                        "seed":seed,"burn_in_transitions":BURN,"postburn_states":DRAWS,
                        "observed_state0_count":count[0],
                        "observed_state1_count":count[1],
                        "observed_state2_count":count[2],
                        "observed_indicator_frequency_exact":str(empirical),
                        "true_indicator_probability_exact":str(pi[2]),
                        "absolute_indicator_estimation_error_exact":str(abs(empirical-pi[2])),
                        "end_state":end
                    })
    if len(exact_rows)!=9288 or len(replicas)!=96 or len(kernel_rows)!=8 or len(world_rows)!=24:
        raise AssertionError("Original frozen universe incomplete")
    file_csv(EXACT,exact_rows)
    file_csv(SAMPLES,replicas)
    file_json(KERNELS,{"research_id":"R195","kernels":kernel_rows,
        "kernel_count":8,"stationary_mean_observations_N":N})
    report={
        "research_id":"R195",
        "evidence":"E1_ARTIFICIAL_EXACT_THREE_STATE_METROPOLIS_HASTINGS",
        "world_count":24,"exact_kernel_count":8,"exact_distribution_cell_count":9288,
        "time_horizon_t0_through_t128":129,
        "seeded_replica_paths":96,"replica_postburn_length":DRAWS,"replica_burn_transitions":BURN,
        "true_stationary_indicator_N_for_finite_ESS":N,
        "MH_direct_accept_reject_vs_conductance_Fraction_agree":True,
        "target_stationarity_and_detailed_balance_exact":True,
        "full_evolution_iteration_and_selected_matrix_power_exact":True,
        "ESS_stationary_covariance_vs_occupancy_moment_DP_exact":True,
        "all_128_step_TV_trajectories_nonincreasing":True,
        "MC_sampling_random_seeds_only_artificial_not_guaranteed_convergence":True,
        "prelocked_BIMODAL_start0":[w for w in world_rows if w["target"]=="BIMODAL" and w["start_state"]==0],
        "prelocked_UNIFORM_start0":[w for w in world_rows if w["target"]=="UNIFORM" and w["start_state"]==0],
        "all_24_start_worlds":world_rows,
        "exact_cells_CSV_sha256":sha256(EXACT.read_bytes()).hexdigest(),
        "kernels_and_ESS_sha256":sha256(KERNELS.read_bytes()).hexdigest(),
        "seeded_MC_CSV_sha256":sha256(SAMPLES.read_bytes()).hexdigest(),
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False
    }
    file_json(RESULT,report)
    acceptance={
        "research_id":"R195","state":"CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MCMC",
        "original_worlds":24,"kernels":8,"fraction_distribution_cells":9288,"seeded_paths":96,
        "two_kernel_algorithms_exact":True,"detailed_balance_pi_T_equals_pi_exact":True,
        "all_recurrence_vs_power_checkpoints_exact":True,
        "finite_N64_ESS_two_independent_methods_Fraction_equal":True,
        "unconstrained_MC_sample_errors_retained":True,
        "result_sha256":sha256(RESULT.read_bytes()).hexdigest(),
        "cells_sha256":report["exact_cells_CSV_sha256"],
        "kernels_sha256":report["kernels_and_ESS_sha256"],
        "simulations_sha256":report["seeded_MC_CSV_sha256"],
        "new_E2":0,"new_E3":0,"real_human_or_historical_data":False
    }
    file_json(ACCEPT,acceptance)
    print("R195_ACCEPTED",json.dumps(acceptance,sort_keys=True))
    for k in kernel_rows:
        print("R195_ESS",k["target"],k["proposal_edge_probability_q"],k["stationary_N64_indicator_ESS_float"])
    return report

def archive():
    names=[Path(__file__).name,RESULT.name,EXACT.name,KERNELS.name,SAMPLES.name,ACCEPT.name]
    with zipfile.ZipFile(ZIP,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:
            info=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,(HERE/name).read_bytes())
        info=zipfile.ZipInfo(PROTOCOL.name,date_time=(2026,10,21,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,PROTOCOL.read_bytes())
    print("R195_ZIP_SHA256",sha256(ZIP.read_bytes()).hexdigest())

class TestFiniteMCMC(unittest.TestCase):
    def test_four_targets(self):self.assertEqual(len(TARGETS),4)
    def test_two_proposals(self):self.assertEqual(len(QS),2)
    def test_24_worlds(self):self.assertEqual(4*2*3,24)
    def test_9288_cells(self):self.assertEqual(24*(HORIZON+1)*3,9288)
    def test_96_seeded_paths(self):self.assertEqual(24*REPLICAS,96)
    def test_proposal_symmetric(self):
        for q in QS:
            Q=Q_of(q)
            self.assertTrue(all(Q[i][j]==Q[j][i] for i,j in product(range(3),repeat=2)))
    def test_proposal_rows_normalized(self):
        for q in QS:self.assertTrue(all(sum(row,F(0))==1 for row in Q_of(q)))
    def test_two_independent_kernels(self):
        for name,w in TARGETS:
            for q in QS:self.assertEqual(kernel_A(w,q),kernel_B(w,q))
    def test_all_detailed_balance(self):
        for name,w in TARGETS:
            for q in QS:validate(w,q,kernel_A(w,q))
    def test_uniform_stationary_thirds(self):self.assertEqual(pi_of((1,1,1)),(F(1,3),)*3)
    def test_bimodal_stationary(self):self.assertEqual(pi_of((4,1,4)),(F(4,9),F(1,9),F(4,9)))
    def test_center_stationary(self):self.assertEqual(pi_of((1,4,1)),(F(1,6),F(2,3),F(1,6)))
    def test_all_single_step_stationary(self):
        for name,w in TARGETS:
            for q in QS:self.assertEqual(step(pi_of(w),kernel_A(w,q)),pi_of(w))
    def test_all_positive_diagonal(self):
        for name,w in TARGETS:
            for q in QS:
                T=kernel_A(w,q)
                self.assertTrue(all(T[i][i]>0 for i in range(3)))
    def test_all_neighbors_positive(self):
        for name,w in TARGETS:
            for q in QS:
                T=kernel_A(w,q)
                self.assertTrue(all(T[i][j]>0 for i,j in ((0,1),(1,0),(1,2),(2,1))))
    def test_power_identity_t0(self):
        for name,w in TARGETS:self.assertEqual(mpow(kernel_A(w,QS[0]),0),tuple(delta(i) for i in STARTS))
    def test_power_equals_T_at_t1(self):
        for name,w in TARGETS:
            for q in QS:self.assertEqual(mpow(kernel_A(w,q),1),kernel_A(w,q))
    def test_iterative_vs_powers_all_24(self):
        for name,w in TARGETS:
            for q in QS:
                T=kernel_A(w,q)
                for start in STARTS:
                    cur=delta(start)
                    for t in range(HORIZON+1):
                        if t in CHECKPOINTS:self.assertEqual(cur,mpow(T,t)[start])
                        if t<HORIZON:cur=step(cur,T)
    def test_TV_nonincreasing_24_worlds(self):
        for name,w in TARGETS:
            for q in QS:
                for start in STARTS:evolution(kernel_A(w,q),pi_of(w),start)
    def test_two_independent_ESS_methods_all_eight(self):
        for name,w in TARGETS:
            for q in QS:
                T=kernel_A(w,q);pi=pi_of(w)
                self.assertEqual(ess_covariance(T,pi)[0],ess_additive_DP(T,pi))
    def test_ESS_finite_positive_and_less_64(self):
        for name,w in TARGETS:
            for q in QS:
                e=ess_covariance(kernel_A(w,q),pi_of(w))[1]
                self.assertTrue(0<e<N)
    def test_higher_q_better_ESS_each_frozen_target(self):
        for name,w in TARGETS:
            small=ess_covariance(kernel_A(w,QS[0]),pi_of(w))[1]
            large=ess_covariance(kernel_A(w,QS[1]),pi_of(w))[1]
            self.assertGreater(large,small)
    def test_higher_q_better_t128_max_TV_each_target(self):
        for name,w in TARGETS:
            pi=pi_of(w)
            v=[max(evolution(kernel_A(w,q),pi,s)[-1][2] for s in STARTS) for q in QS]
            self.assertLess(v[1],v[0])
    def test_replay_random_seed_exact(self):
        T=kernel_A((4,1,4),QS[0])
        self.assertEqual(simulate(T,0,195000),simulate(T,0,195000))
    def test_seeded_samples_are_2048(self):
        for name,w in TARGETS:
            count,last=simulate(kernel_A(w,QS[0]),0,195000)
            self.assertEqual(sum(count),2048)
    def test_burn64_not_guaranteed_stationarity(self):
        T=kernel_A((4,1,4),QS[0])
        self.assertNotEqual(evolution(T,pi_of((4,1,4)),0)[64][1],pi_of((4,1,4)))
    def test_same_pi_different_T(self):
        self.assertNotEqual(kernel_A((1,1,1),QS[0]),kernel_A((1,1,1),QS[1]))
    def test_initial_TV_identity(self):
        pi=pi_of((4,1,4))
        self.assertEqual(tv(delta(0),pi),1-pi[0])
    def test_unregistered_weights_fail(self):
        with self.assertRaises(ValueError):kernel_A((2,2,2),QS[0])
    def test_unregistered_q_fail(self):
        with self.assertRaises(ValueError):kernel_A((1,1,1),F(1,10))
    def test_invalid_initial_fail(self):
        with self.assertRaises(ValueError):delta(4)
    def test_outside_horizon_fail(self):
        with self.assertRaises(ValueError):mpow(kernel_A((1,1,1),QS[0]),129)
    def test_modified_kernel_rejected(self):
        T=[list(row) for row in kernel_A((1,4,1),QS[0])]
        T[0][0]-=F(1,32)
        T[0][1]+=F(1,32)
        with self.assertRaises(AssertionError):validate((1,4,1),QS[0],tuple(tuple(row) for row in T))

if __name__=="__main__":
    if sys.argv[1:]==["--test"]:
        unittest.main(argv=[sys.argv[0]],verbosity=2)
    elif sys.argv[1:]==["--run-and-archive"]:
        run();archive()
    else:raise SystemExit("Use --test or --run-and-archive")
