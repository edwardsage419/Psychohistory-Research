#!/usr/bin/env python3
"""R063 independent summary of Najar (2020) original Figure 6 source CSVs.

Values below are transcribed from exact GitHub blob source and are AUTHOR
FIGURE DERIVED ESTIMATES, not trial-by-trial human choices or this project's fits.
External dependency scipy is optional. IDs are omitted; for Exp1 the published
file has identically ordered paired participant IDs 3..26 for both conditions.
"""
import json, statistics

FIG6_SOURCE = {
 'exp1': {'fig6a':'24fcb06ac21b6dfc168574064585342e3c549b82',
          'fig6b':'3567d744db1d51e02477b726051fe0ddc9d51de6'},
 'exp2': {'fig6a':'9b9d70b88f6efebe550c4a20b7a70cb0a461950a',
          'fig6b':'848492f1764550f40d6ad05aaead3e2a2f5e646e'}
}
SOURCE_COMMIT='554ee8007ff6fd1c51cd68d7d254f22a34e6dab1'
FREQ={
 'exp1':{'VS':.260598029224976, 'metaVS':.739401970775024,
          'XP_VS':.0108,'XP_metaVS':.9892},
 'exp2':{'VS':.405894113927188, 'metaVS':.594105886072812,
          'XP_VS':.0997,'XP_metaVS':.9003},
}
RATE={
 'exp1':{
  'skilled':[.0042390136,.049787894125,.0028688662375,.04779855975,.7301366075425,.00182658995,.0135209795,.0585075105,.5835827220875,.086704265,.1183129975,.042175247625,.011327235375,.055570939375,.07555999375,.059460962125,.04736479775,.014096133625,.042835505375,.0018579342125,.063146162,.0661204885,.021840755125,.033639634],
  'unskilled':[.0016720528125,.01906185825,.00112468055,.0194392715,.427237704924275,.000692594875,.00674493025,.024116672375,.351540917559875,.04045718125,.055911165,.01544414625,.005569217625,.03080789175,.05215421125,.021373766375,.01822230375,.00568752425,.019659279625,.0009311365125,.02638212075,.030568577,.0104151545,.02191511],
 },
 'exp2':{
  'skilled':[.242657228333333,.635898702325833,.023671891416667,.0172420235,.557950350444973,.592832541666667,.553762016613063,.588464590910209,.13198524,.0636449475,.05858717275,.027569064,.192437174166667,.594567949158333,.038629494416667,.120583750833333,.563232155333333,.018566568583333,.206151155833333,.655244916353905,.03577191875,.571838404166667],
  'unskilled':[.023577589333333,.003468369216667,.001585543666667,.004818782333333,.000835507558333,.212096951666667,.011366681083333,.000187124945833,.017475472833333,.072907070833333,.1904636,.509521688691667,.019901481583333,.105115805,.004733132166667,.0002009695,.024540883583333,.002597259116667,.007239605916667,.025186970166667,.393035837025,.360710951583333],
 },
}

def summarize():
    r={}
    for exp, groups in RATE.items():
        s,u=groups['skilled'],groups['unskilled']
        row={'provenance':'AUTHOR_FIGURE_DERIVED_VALUES','source':FIG6_SOURCE[exp],
             'model_frequency':FREQ[exp],
             'skilled':{'n':len(s),'mean':statistics.mean(s),'median':statistics.median(s)},
             'unskilled':{'n':len(u),'mean':statistics.mean(u),'median':statistics.median(u)},
             'mean_difference':statistics.mean(s)-statistics.mean(u)}
        if exp=='exp1':
            differences=[a-b for a,b in zip(s,u)]
            row['paired_difference_mean']=statistics.mean(differences)
            row['paired_positive_n']=sum(d>0 for d in differences)
        try:
            from scipy.stats import wilcoxon, mannwhitneyu
            if exp=='exp1':
                test=wilcoxon(s,u,alternative='two-sided',method='exact')
                row['wilcoxon_two_sided_p']=float(test.pvalue)
            else:
                test=mannwhitneyu(s,u,alternative='two-sided',method='exact')
                row['mann_whitney_two_sided_p']=float(test.pvalue)
                row['mann_whitney_U_unskilled']=float(mannwhitneyu(u,s,alternative='two-sided',method='exact').statistic)
        except ImportError:
            row['optional_scipy_stats']='SKIPPED'
        r[exp]=row
    return r

if __name__=='__main__':
    print(json.dumps({'source_commit':SOURCE_COMMIT,'results':summarize()},ensure_ascii=False,indent=2))
