#!/usr/bin/env Rscript
# Exact author make_el and convert_to_hh execution; each original R function is
# evaluated from hash-pinned public R source; only runner-local edges are written.
args <- commandArgs(trailingOnly=TRUE)
if (length(args) != 3) stop("usage: Rscript parity.R data.tab author.R output.tsv")
source_data <- args[[1]]
source_r <- args[[2]]
target_file <- args[[3]]

check_source <- function(path, size_expected, sha_expected) {
  if (file.info(path)$size != size_expected) stop("original source byte size differs")
  sha <- system2("sha256sum", shQuote(path), stdout=TRUE)
  if (length(sha) != 1 ||
      strsplit(sha, " +")[[1]][[1]] != sha_expected) {
    stop("author source sha256 mismatch")
  }
}
check_source(source_data, 444658,
  "10b3e31a6d160e003ff9edf96fc1f6e1a8549ea547b8b8b08aadab1f52b40cae")
check_source(source_r, 72914,
  "2e7b7b22887c69c057a6f2fa1a1ff393566826fdb19e6aad6360393ea9f86ff2")

source_lines <- readLines(source_r, warn=FALSE, encoding="UTF-8")
extract_author_function <- function(name) {
  positions <- grep(paste0("^", name, " <- function\\("), source_lines)
  if (length(positions) != 1) stop(paste("author function selector not unique",name))
  depth <- 0L
  started <- FALSE
  end <- NA_integer_
  for (line_idx in seq.int(positions[[1]],length(source_lines))) {
    line <- strsplit(source_lines[[line_idx]], "#", fixed=TRUE)[[1]][1]
    opened <- nchar(gsub("[^{]", "", line))
    closed <- nchar(gsub("[^}]", "", line))
    if (opened > 0) started <- TRUE
    depth <- depth + opened - closed
    if (started && depth == 0) {end <- line_idx; break}
  }
  if (is.na(end)) stop("original function body incomplete")
  src <- paste(source_lines[seq.int(positions[[1]],end)],collapse="\n")
  parsed <- parse(text=src)
  if(length(parsed)!=1) stop("original author function parse not unique")
  eval(parsed, envir=.GlobalEnv)
  fn <- get(name, envir=.GlobalEnv)
  if (!is.function(fn)) stop("original source function not callable")
}
extract_author_function("make_el")
extract_author_function("convert_to_hh")

DF <- read.delim(source_data,header=TRUE,sep="\t",quote="",
                 check.names=FALSE,colClasses="character",stringsAsFactors=FALSE,
                 na.strings=c("", "NA", "NaN", "\\N", "."))
if (nrow(DF) != 2125 || ncol(DF) != 66 ||
    length(unique(DF$village_number)) != 16) stop("source universe mismatch")

nomination <- list(
  visit=paste0("visit",1:5),
  meal=paste0("meal",1:5),
  borrow=paste0("borrow",1:5),
  rumor=paste0("rumor",1:5))
members <- c("ego","hhh",paste0("hh",1:11))
all_edges <- list()
edge_count <- 0L

# The original R author sorts within each village by hhnum before building
# network nodes. We retain original author function bodies exactly.
for (village in unique(DF$village_number)) {
  df <- DF[DF$village_number==village, , drop=FALSE]
  hhnum <- suppressWarnings(as.numeric(df$hhnum))
  if (any(is.na(hhnum))) stop("household sort cannot resolve numeric hhnum")
  df <- df[order(hhnum),,drop=FALSE]
  df[, c(members,unlist(nomination))] <-
    lapply(df[,c(members,unlist(nomination)),drop=FALSE],function(col) {
      col[is.na(col)] <- ""
      col
    })
  familymat <- as.matrix(df[, members, drop=FALSE])
  household_list <- lapply(seq_len(nrow(df)),function(i) {
    present <- which(familymat[i,] != "")
    unique(familymat[i,present])
  })
  for (category in names(nomination)) {
    alters <- lapply(nomination[[category]],function(name) df[[name]])
    el <- make_el(data=df,ego=df$ego,alter_list=alters)
    if (length(el)==0 || nrow(as.matrix(el))==0) next
    hh <- convert_to_hh(household_list,el)
    if (is.null(hh) || length(hh)==0) next
    if (!is.matrix(hh)) hh <- matrix(hh,ncol=2)
    if (ncol(hh)!=2 || any(is.na(hh))) stop("original household source output invalid")
    hh <- apply(hh,2,as.integer)
    if (!is.matrix(hh)) hh <- matrix(hh,ncol=2)
    if (ncol(hh)!=2 || any(hh<1) || any(hh>nrow(df))) stop("bad original household references")
    hh <- hh[hh[,1] != hh[,2],,drop=FALSE]
    if (!nrow(hh)) next
    minimum <- pmin(hh[,1],hh[,2])
    maximum <- pmax(hh[,1],hh[,2])
    tuples <- unique(data.frame(
      village=rep(as.character(village),length(minimum)),
      category=rep(category,length(minimum)),
      smaller=minimum,
      larger=maximum,
      stringsAsFactors=FALSE))
    edge_count <- edge_count + nrow(tuples)
    if (edge_count > 100000) stop("source edge count exceeds cap")
    all_edges[[length(all_edges)+1]] <- tuples
  }
}
if (!length(all_edges)) stop("author source R yielded zero edges")
edges <- unique(do.call(rbind,all_edges))
write.table(edges,file=target_file,sep="\t",row.names=FALSE,
            col.names=FALSE,quote=FALSE,na="")
cat("ORIGINAL_AUTHOR_R_CORE_EXECUTED_VILLAGES=16\n")
cat("ORIGINAL_AUTHOR_R_CORE_EDGE_COUNT=",nrow(edges),"\n",sep="")
cat("ORIGINAL_AUTHOR_R_CORE_NO_RESPONDENT_DATA_LOGGED=TRUE\n")
