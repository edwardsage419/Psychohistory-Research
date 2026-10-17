# R075 third external human experimental dataset, third-party source admissibility.
# No human-level decisions or IDs shall be emitted by this script.

audit_frd <- function(x, expected_rows=NULL) {
  required <- c("treatment","id","game","period","last.choice",
                "last.other","choice","bc","error")
  if (!is.data.frame(x) || !setequal(names(x),required))
    stop("SOURCE_NINE_FIELDS_DIFFER")
  if (!is.null(expected_rows) && nrow(x)!=expected_rows)
    stop("SOURCE_ROW_COUNT_DIFFERS")
  if (anyNA(x[,c("treatment","id","game","period","choice","bc","error")]))
    stop("SOURCE_KEYS_ACTION_OR_POLICY_MISSING")
  if (!all(as.character(x$choice) %in% c("c","d")))
    stop("CHOICE_NOT_BINARY")
  if (!all(is.finite(as.numeric(x$period)) |
           is.na(as.numeric(x$period))))
    stop("PERIOD_NONFINITE")
  if (!all(as.numeric(x$period)>=1) ||
      any(as.numeric(x$period)!=as.integer(x$period)))
    stop("PERIOD_NOT_POSITIVE_INTEGER")
  treatment <- as.character(x$treatment)
  groups <- split(seq_len(nrow(x)),
                  interaction(treatment,as.character(x$id),as.character(x$game),
                              drop=TRUE))
  if (!length(groups))stop("EMPTY_HUMAN_SOURCE")
  duplicate_rounds <- 0L
  incomplete_games <- 0L
  checked <- mismatch <- lag_own_missing <- lag_other_missing <- 0L
  eligible <- 0L
  first_round_lag_nonmissing <- 0L
  treatment_levels <- sort(unique(treatment))
  lag_checked_by_treatment <- setNames(integer(length(treatment_levels)),treatment_levels)
  lag_mismatch_by_treatment <- setNames(integer(length(treatment_levels)),treatment_levels)
  for(ix in groups) {
    ord <- order(as.numeric(x$period[ix]))
    ix <- ix[ord]
    periods <- as.integer(x$period[ix])
    if (anyDuplicated(periods))duplicate_rounds <- duplicate_rounds+1L
    if (!identical(periods,seq_len(length(periods))))
      incomplete_games <- incomplete_games+1L
    first_round_lag_nonmissing <- first_round_lag_nonmissing+
      as.integer(!is.na(x$last.choice[ix[1]]) || !is.na(x$last.other[ix[1]]))
    if(length(ix)<2)next
    for(k in 2:length(ix)) {
      if(periods[k]!=periods[k-1]+1L)next
      checked <- checked+1L
      lag_checked_by_treatment[treatment[ix[1]]] <- lag_checked_by_treatment[treatment[ix[1]]]+1L
      if(is.na(x$last.choice[ix[k]])) {
        lag_own_missing <- lag_own_missing+1L
      }else if(as.character(x$last.choice[ix[k]])!=as.character(x$choice[ix[k-1]])) {
        mismatch <- mismatch+1L
        lag_mismatch_by_treatment[treatment[ix[1]]] <- lag_mismatch_by_treatment[treatment[ix[1]]]+1L
      }
      if(is.na(x$last.other[ix[k]]))lag_other_missing <- lag_other_missing+1L
      if(k>=3 && periods[k-1]==periods[k]-1 &&
         periods[k-2]==periods[k]-2 &&
         !anyNA(x$last.other[ix[(k-1):k]]))eligible<-eligible+1L
    }
  }
  treatments <- sort(unique(treatment))
  per_treatment <- lapply(treatments,function(tr) {
     ix <- which(treatment==tr)
     list(treatment=tr,
          original_rows=length(ix),
          persons=length(unique(as.character(x$id[ix]))),
          person_games=length(unique(paste(as.character(x$id[ix]),x$game[ix],sep=":"))),
          bc_categories=paste(sort(unique(as.character(x$bc[ix]))),collapse="|"),
          error_categories=paste(sort(unique(as.character(x$error[ix]))),collapse="|"),
          adjacent_lag_checks=as.integer(lag_checked_by_treatment[tr]),
          own_previous_vs_choice_mismatch=as.integer(lag_mismatch_by_treatment[tr]),
          mismatch_rate=if(lag_checked_by_treatment[tr]>0) unname(lag_mismatch_by_treatment[tr]/lag_checked_by_treatment[tr]) else NA_real_)
  })
  list(
      total_rows=nrow(x),
      treatment_count=length(treatments),
      unique_treatment_id=length(unique(paste(treatment,as.character(x$id),sep=":"))),
      subject_game_groups=length(groups),
      row_duplicate_groups=duplicate_rounds,
      non_contiguous_subject_games=incomplete_games,
      adjacent_history_checks=checked,
      previous_own_action_mismatch=mismatch,
      previous_own_action_missing=lag_own_missing,
      previous_opponent_action_missing=lag_other_missing,
      first_round_lag_present_groups=first_round_lag_nonmissing,
      structurally_scorable_t3_events=eligible,
      original_session_field_present=("session" %in% names(x)),
      per_treatment=per_treatment
  )
}

write_frd_public_tsv <- function(x,path) {
  header <- c("scope","total_rows","treatment_count","unique_treatment_id",
    "subject_game_groups","row_duplicate_groups","non_contiguous_subject_games",
    "adjacent_history_checks","previous_own_action_mismatch",
    "previous_own_action_missing","previous_opponent_action_missing",
    "first_round_lag_present_groups","structurally_scorable_t3_events",
    "original_session_field_present")
  values <- vapply(header[-1],function(n) as.character(x[[n]]),character(1))
  writeLines(c(paste(header,collapse="\t"),
               paste(c("overall",values),collapse="\t")),path)
  # No treatment- or player-level lines in public file.
}

if(sys.nframe()==0) {
  args <- commandArgs(trailingOnly=TRUE)
  if(length(args)!=2)stop("USAGE_R075_DATALOCATION_AND_PUBLIC_TSV")
  env <- new.env(parent=baseenv())
  names_loaded <- load(args[[1]],envir=env)
  if(!identical(names_loaded,"FRD2012"))stop("RDATA_OBJECT_NAME_MISMATCH")
  x <- get("FRD2012",envir=env)
  summary <- audit_frd(x,13126L)
  write_frd_public_tsv(summary,args[[2]])
  print(summary[setdiff(names(summary),"per_treatment")])
  cat("per_treatment_aggregate_no_identifiers\n")
  for(tr in summary$per_treatment)cat(
      paste(tr$treatment,tr$original_rows,tr$persons,tr$person_games,
            tr$bc_categories,tr$error_categories,tr$adjacent_lag_checks,
            tr$own_previous_vs_choice_mismatch,tr$mismatch_rate,sep="\t"),"\n",sep="")
  cat("R075_THIRD_PARTY_SCHEMA_AUDIT_ONLY; no model scored; original session absent\n")
}
