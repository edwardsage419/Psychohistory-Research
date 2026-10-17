source("r075_frd2012_lag_schema_audit.R")
build <- function() data.frame(
    treatment=rep("1",4),
    id=rep("101",4),
    game=rep(1L,4),
    period=1:4,
    last.choice=c(NA,"c","d","c"),
    last.other=c(NA,"c","d","c"),
    choice=c("c","d","c","c"),
    bc=rep("2",4),
    error=rep("0",4)
)
x<-build()
s<-audit_frd(x)
stopifnot(s$total_rows==4)
stopifnot(s$unique_treatment_id==1)
stopifnot(s$subject_game_groups==1)
stopifnot(s$adjacent_history_checks==3)
stopifnot(s$previous_own_action_mismatch==0)
stopifnot(s$previous_opponent_action_missing==0)
stopifnot(s$structurally_scorable_t3_events==2)
stopifnot(!s$original_session_field_present)

m<-build()
m$last.choice[3]<-"c"
stopifnot(audit_frd(m)$previous_own_action_mismatch==1)

n<-build()
n$last.other[3]<-NA
stopifnot(audit_frd(n)$previous_opponent_action_missing==1)
stopifnot(audit_frd(n)$structurally_scorable_t3_events==0)

d<-build()
d$period[3]<-2
stopifnot(audit_frd(d)$row_duplicate_groups==1)
stopifnot(audit_frd(d)$non_contiguous_subject_games==1)

f<-build()
f$period[3]<-5
stopifnot(audit_frd(f)$non_contiguous_subject_games==1)

q<-build()
q$choice[4]<-"x"
stopifnot(inherits(try(audit_frd(q),silent=TRUE),"try-error"))

z<-build()
z$session<-"1"
stopifnot(inherits(try(audit_frd(z),silent=TRUE),"try-error"))

u<-build()
u<-rbind(u,transform(u,id="102"))
stopifnot(audit_frd(u)$unique_treatment_id==2)
stopifnot(audit_frd(u)$structurally_scorable_t3_events==4)

cat("R075_SYNTHETIC_LAG_SOURCE_SCHEMA_TESTS_PASS=13\n")
