* Democratic Trajectories in the Third Wave: Aligning Theory and Methods
* Aníbal Pérez-Liñán and Scott Mainwaring
* British Journal of Political Science
* February 9, 2025

 use "0_Trajectories.dta", clear
 
 xtset id2 t
  
 gen brmark = libdem if breakdown==1 // labels for figures
 gen figs = 1 if (  ///
   id == "ARG1984" | ///
   id == "BRA1986" | ///
   id == "NIC1990" | ///
   id == "GHA1996" | ///
   id == "SEN1983" | ///
   id == "HUN1990" | ///
   id == "IND1977" | ///
   id == "KOR1988" | ///
   id == "SRB2000" | ///
   id == "TUR1987" | ///
    ) 
 
  * Characteristics of liberal democracy (text)
  /*
  sum libdem if t==0
  sum libdem if t==0 & libdem > 36 & libdem < 56
  di 62/102
  tab libdem if t==0
  sum libdem if t==10
  di 64/102
  */
    
 * Argentina and South Korea (text)
 * list country_text_id year libdem gdpg if (country_text_id=="ARG" | country_text_id=="KOR") & (t==0 | year==2017)
 
	
*********************************** ANALYSIS ***********************************

* Create variable shells for Level 1
 gen          dreg_   = .
    label var dreg_ "Regional democracy" 
 gen          gdpt_   = .
    label var gdpt_   "Per cap GDP (ths)" 
 gen          gdpg_   = .
    label var gdpg_   "Economic growth" 
 gen          gini_   = .
    label var gini_   "Gini index" 
 gen          scap_   = .
    label var scap_   "State capacity" 
 gen         insample = .
 label var t " "

* Model specification
macro drop _all
 global Trend   c.t##c.t##c.t
 global Level1  c.gdpg_ c.gdpt_ c.gini_ c.scap_ c.dreg_   // Use shells rather than varnames
 global Level2  c.gdpgM c.gdptM c.giniM c.scapM c.dregM c.t0 
		
* Create interaction terms for model 3b [replicates M3 with manual interactions, for table]
  gen t2 = t*t
   label var t2 "Years^2"
  gen t3 = t*t*t
   label var t3 "Years^3"
  foreach T in t t2 t3 {
   foreach X in gdpgM gdptM giniM scapM dregM t0  {
      gen `T'_`X' = `T'*`X'  
	  local lbl : variable label `X'
	  label var `T'_`X' " *`lbl'"
   }
  }
				 
 * M1: Fixed-effects
 
   replace dreg_ = dregion
   replace gdpt_ = gdpt
   replace gdpg_ = gdpg
   replace gini_ = gini
   replace scap_ = scapacity
 
 xtreg libdem $Level1 , fe
   est store M1
  predict    y_m1u, xbu
   label var y_m1u "Predicted (M1, unit effects)"
   * Root Mean Square Error
     gen  e2_y_m1u = (libdem - y_m1u)^2
	 sum  e2_y_m1u, meanonly
	 scalar rmse_m1u = sqrt(r(mean))
	 di rmse_m1u
 
   
 * M2: Hybrid model
 
   replace dreg_ = dregC
   replace gdpt_ = gdptC
   replace gdpg_ = gdpgC
   replace gini_ = giniC
   replace scap_ = scapC
  
 mixed libdem $Level1 $Level2 || id:
   est store M2
  predict    y_m2
   label var y_m2 "Predicted (M2, no random effects)"
  predict    y_m2u, fitted
   label var y_m2u "Predicted (M2, unit effects)"
   * Root Mean Square Error
     gen  e2_y_m2u = (libdem - y_m2u)^2
	 sum  e2_y_m2u, meanonly
	 scalar rmse_m2u = sqrt(r(mean))
	 di rmse_m2u
 
 
 * M3: Latent growth curve
 
 mixed libdem $Level1 ($Trend)##($Level2) || id: $Trend 
  est store M3
  replace insample = e(sample)
 
 * M3b: replicate with manually created interactions
  mixed libdem  gdpg_    gdpt_   gini_    scap_   dreg_          ///
                gdpgM    gdptM   giniM    scapM   dregM      t0  ///
        t     t_gdpgM  t_gdptM t_giniM  t_scapM t_dregM    t_t0  ///
		t2   t2_gdpgM t2_gdptM t2_giniM t2_scapM t2_dregM t2_t0  ///
        t3   t3_gdpgM t3_gdptM t3_giniM t3_scapM t3_dregM t3_t0  ///
        || id: t t2 t3
  est store M3b
  predict    y_m3
   label var y_m3 "Predicted (M3, no random effects)"
  predict    y_m3u, fitted
   label var y_m3u "Predicted (M3, random effects)"
   * Root Mean Square Error
     gen  e2_y_m3u = (libdem - y_m3u)^2
	 sum  e2_y_m3u, meanonly
	 scalar rmse_m3u = sqrt(r(mean))
	 di rmse_m3u
	 
	lrtest M3 M2, stats
 
 * Table 1
 esttab M1 M2 M3b ///
      using "Table1.rtf", ///
	  cell((b(star fmt(%8.3f)) se(par))) wide compress ///
	  star(* 0.05) legend label   ///
	  varwidth(25) modelwidth(7) nomtitles interaction(" ") ///
	  stats ( N , fmt(%9.0g %9.1f) labels("N" ) )  ///
	  title("Table 1. Alternative Panel Models") replace ///
	   varlabels( t "Years since transition" _cons "Intercept")
	
	
 *** Figure 1 - Graphs comparing models ***

 * sizes page
   global xs = 7.5 
   global ys = 5
 
preserve
  keep if figs==1
 twoway (scatter libdem t, symbol(|) msize(small) mc(gs8) by(id, note("") legend(off) cols(5) com) xsize($xs) ysize($ys) )  ///
        (scatter brmark t, symbol(o) mlcolor(gs0) subtitle(,nobox bc(none) size(vlarge))    /// 
		         xlabel(, alternate labs(large)) xtitle("") ylabel(0(50)100, labs(large)) ) ///
		(scatter y_m3u  t, connect(ascending) symbol(none) lc(gs0)   lp(solid) )   ///
		(scatter y_m2u  t, connect(ascending) symbol(none) lc(gs2) lp(dash) )
  graph export "Figure1.png", replace width(1000)		
restore		

 * % Change in the Root Mean Square Error
 di "RMSE M2.1:" %8.2f rmse_m1u ", M2.2:" %8.2f rmse_m2u ", M2.3:" %8.2f rmse_m3u
 scalar d_21 = 100*(rmse_m2u - rmse_m1u)/rmse_m1u // m2 vs m1
     di %8.2f d_21
 scalar d_31 = 100*(rmse_m3u - rmse_m1u)/rmse_m1u // m3 vs m1
     di %8.2f d_31
 scalar d_32 = 100*(rmse_m3u - rmse_m2u)/rmse_m2u // m3 vs m2
     di %8.2f d_32
 
 
 *** Figure 2 - Graphs for latent curve ***
 
 est restore M3
 label drop _all
 
 * Trend by Growth
 label define lgdpgM 1 "1% growth" 5 "5% growth"
 label values            gdpgM lgdpgM
 margins, at(t=(0(2)10)  gdpgM=(1 5)) noestimcheck
 marginsplot, recastci(rarea) recast(line) yscale(r(0(10)100)) ylabel(0(50)100) ///
  ytitle("") title("2.1. Economic Growth") xsize(6) ysize(3) ///
  legend(region(lcolor(none)))
  graph save "pred3.gph", replace
  
  * Trend by GDP 
 label define lgdptM 2 "$2,000" 5 "$5,000" 20 "$20,000"
 label values            gdptM lgdptM
 margins, at(t=(0(2)10)  gdptM=(5 20)) noestimcheck
 marginsplot, recastci(rarea) recast(line) yscale(r(0(10)100)) ylabel(0(50)100) ///
  ytitle("") title("2.2. Gross Domestic Product") xsize(6) ysize(3) ///
  legend(region(lcolor(none)))
    graph save "pred2.gph", replace

* Trend by Gini
 label define lginiM 30 "Gini = 30" 60 "Gini = 60"
 label values            giniM lginiM
 margins, at(t=(0(2)10)  giniM=(30 60)) noestimcheck
 marginsplot, recastci(rarea) recast(line) yscale(r(0(10)100)) ylabel(0(50)100) ///
  ytitle("") title("2.3. Inequality") xsize(6) ysize(3) ///
  legend(region(lcolor(none)))
  graph save "pred4.gph", replace
  
* Trend by State Capacity
 label define lscapM 35 "Low (35)" 65 "High (65)"
 label values            scapM lscapM
 margins, at(t=(0(2)10)  scapM=(35 65)) noestimcheck
 marginsplot, recastci(rarea) recast(line) yscale(r(0(10)100)) ylabel(0(50)100) ///
  ytitle("") title("2.4. State Capacity") xsize(6) ysize(3) ///
  legend(region(lcolor(none)))
  graph save "pred5.gph", replace
  
* Trend by regional democracy 
 label define ldregM 40 "40% democracies" 70 "70%"
 label values            dregM ldregM
 margins, at(t=(0(2)10)  dregM=(40 70)) noestimcheck
 marginsplot, recastci(rarea) recast(line) yscale(r(0(10)100)) ylabel(0(50)100) ///
  ytitle("") title("2.5. Regional Democracy") xsize(6) ysize(3) ///
  legend(region(lcolor(none)))
  graph save "pred1.gph", replace
  
 * Trend by year of transition
 label define lt0 1985 "In 1985" 2005 " In 2005"
 label values            t0 lt0
 margins, at(t=(0(2)10)  t0=(1985 2005)) noestimcheck
 marginsplot, recastci(rarea) recast(line) yscale(r(0(10)100)) ylabel(0(50)100) ///
  ytitle("") title("2.6. Transition Year") xsize(6) ysize(3) ///
  legend(region(lcolor(none)))
  graph save "pred6.gph", replace
  
  global pagesize rows(3) xsize(7.5) ysize(10)
  
  graph combine "pred3.gph" "pred2.gph" ///
                "pred4.gph" "pred5.gph" ///
				"pred1.gph" "pred6.gph", ///
				ycommon $pagesize
  graph export "Figure2.png", replace width(1000)				
				
				
************************* Supplementary Materials ******************************

** Table S2 - Descriptive Statistics
tabstat libdem gdpg  gdpt  gini  scapacity dregion t, columns(statistics) stats(mean min max sd n) format(%6.1f)
tabstat        gdpgM gdptM giniM scapM     dregM   t0 if t==0, columns(statistics) stats(mean min max sd n) format(%6.1f)


** Table S3 - Alternative Polynomial Specifications for the Latent Growth Curve
* S30: No curve
  mixed libdem                || id: 
  est store A30
* S31: Linear
  mixed libdem  t             || id: t   
  est store A31
* S32: Quadratic
  mixed libdem  t t2          || id: t t2 
  est store A32
* S33: Cubic
  mixed libdem  t t2 t3       || id: t t2 t3 
  est store A33
* S34: Quartic
  gen t4 = t^4
  mixed libdem  t t2 t3 t4    || id: t t2 t3 t4
  est store A34
* S35: Quintic
  gen t5 = t^5
  mixed libdem  t t2 t3 t4 t5 || id: t t2 t3 t4 t5
  est store A35    
* Likelihood ratio tests
  lrtest A31 A30, stats
  lrtest A32 A31, stats
  lrtest A33 A32, stats
  lrtest A34 A33, stats
  lrtest A35 A34, stats

  
** Table S4 - Nested Growth Curve Models (listed in reverse for esample)

* S43: M2.3 with manually created interactions (same as M3b)
  mixed libdem  gdpg_    gdpt_   gini_    scap_   dreg_          ///
                gdpgM    gdptM   giniM    scapM   dregM      t0  ///
        t     t_gdpgM  t_gdptM t_giniM  t_scapM t_dregM    t_t0  ///
		t2   t2_gdpgM t2_gdptM t2_giniM t2_scapM t2_dregM t2_t0  ///
        t3   t3_gdpgM t3_gdptM t3_giniM t3_scapM t3_dregM t3_t0  ///
        || id: t t2 t3
  est store A43
  gen sampleA4 = 1 if e(sample)

  * S42: Only level-2 predictors
  mixed libdem                                                   ///
                gdpgM    gdptM   giniM    scapM   dregM      t0  ///
        t     t_gdpgM  t_gdptM t_giniM  t_scapM t_dregM    t_t0  ///
		t2   t2_gdpgM t2_gdptM t2_giniM t2_scapM t2_dregM t2_t0  ///
        t3   t3_gdpgM t3_gdptM t3_giniM t3_scapM t3_dregM t3_t0  ///
		if sampleA4 == 1                                         ///
        || id: t t2 t3
  est store A42
  
   * S41: Baseline
  mixed libdem                                                   ///              
        t                                                        ///
		t2                                                       ///
        t3                                                       ///
		if sampleA4 == 1                                         ///
        || id: t t2 t3
  est store A41
  
  * Likelihood ratio tests
  lrtest A42 A41, stats
  lrtest A43 A41, stats
  lrtest A43 A42, stats
 
 * Table S4 - (M3b is redundant, just creates structure for table)
 esttab M3b A41 A42 A43 ///
      using "TableS4.rtf", ///
	  cell((b(star fmt(%8.1f)) se(par))) wide compress ///
	  star(* 0.05) legend label   ///
	  varwidth(25) modelwidth(7) nomtitles interaction(" ") ///
	  stats ( N , fmt(%9.0g %9.1f) labels("N") )  ///
	  title("Table S4. Nested Growth Curve Models") replace ///
	   varlabels( t "Years since transition" _cons "Intercept")

	   
** Table S5 - Extended fixed-effects models

* Use original level-1 variables for shells
   replace dreg_ = dregion
   replace gdpt_ = gdpt
   replace gdpg_ = gdpg
   replace gini_ = gini
   replace scap_ = scapacity

* TWFE with year dummies    
xtreg libdem $Level1 i.year, fe
  est store A51
   * Root Mean Square Error
    predict    y_A51, xbu
    label var  y_A51 "Predicted (A51, TWFE)"
     gen  e2_y_A51 = (libdem - y_A51)^2
	 sum  e2_y_A51, meanonly
	 scalar rmse_A51 = sqrt(r(mean))
	 di     rmse_A51

* FE with cumulative mean growth variable
  * Compute cumulative variable for growth
  sort id2 t
  by id2: gen cumg = sum(gdpg)
  gen       cumgdpg = cumg/(t + 1)
  label var cumgdpg "Cumulative growth, mean"
  order gdpg cumgdpg, last
	 
xtreg libdem $Level1 cumgdpg, fe
  est store A52
   * Root Mean Square Error
    predict    y_A52, xbu
    label var  y_A52 "Predicted (A52, Cumulative)"
     gen  e2_y_A52 = (libdem - y_A52)^2
	 sum  e2_y_A52, meanonly
	 scalar rmse_A52 = sqrt(r(mean))
	 di     rmse_A52  

* Dynamic panel model with FE
  * Compute lag for dynamic model	 
  gen libdem_1 = l.libdem
  label var libdem_1 "Democracy, t-1"
	 
xtreg libdem $Level1 libdem_1, fe
  est store A53
   * Root Mean Square Error
    predict    y_A53, xbu
    label var  y_A53 "Predicted (A53, Dynamic)"
     gen  e2_y_A53 = (libdem - y_A53)^2
	 sum  e2_y_A53, meanonly
	 scalar rmse_A53 = sqrt(r(mean))
	 di     rmse_A53 	 
	 
* Table S5 - 
 esttab M3 A51 A52 A53 ///
      	 using "TableS5.rtf", replace ///
		 b(3) se(3) compress ///
	  star(* 0.05) legend label    ///
	  varwidth(25) modelwidth(7) nomtitles interaction(" ") ///
	  stats ( N , fmt(%9.0g %9.1f) labels("N") )  ///
	  title("Table S5. Extended Fixed-Effects Models")  ///
	  keep(gdpg_ gdpt_ gini_ scap_ dreg_ cumgdpg libdem_1 _cons) ///
	  varlabels( _cons "Intercept")
* Root mean squared errors
  di %9.3f rmse_m3u
  di %9.3f rmse_A51
  di %9.1f 100*(rmse_A51 - rmse_m3u)/rmse_m3u
  di %9.3f rmse_A52
  di %9.1f 100*(rmse_A52 - rmse_m3u)/rmse_m3u
  di %9.3f rmse_A53
  di %9.1f 100*(rmse_A53 - rmse_m3u)/rmse_m3u
 
 
** Table S6 - Instrumental variables **

* Restore centered variables to shells	  
   replace dreg_ = dregC
   replace gdpt_ = gdptC
   replace gini_ = giniC
   replace scap_ = scapC
	  
* Measure of growth "purged" from the effects of democracy	  
reg gdpg l.libdem
   predict gdpgi, residuals
   label var gdpgi "Growth instrument"	
   corr gdpg gdpgi
   
* S61   
* New measures of growth
  by id2: egen gdpgMi = mean(gdpgi) 
  label var    gdpgMi "Growth inst (mean)"   
  gen          gdpgCi = gdpgi - gdpgMi
  label var    gdpgCi "Growth inst (centered)" 
  
* Replace shells with new measures of growth  
   replace gdpg_ = gdpgCi   
   replace gdpgM = gdpgMi

* New model with "purged" measure of growth
   mixed libdem  gdpg_    gdpt_   gini_    scap_   dreg_          ///
                 gdpgM    gdptM   giniM    scapM   dregM      t0  ///
         t     t_gdpgM  t_gdptM t_giniM  t_scapM t_dregM    t_t0  ///
		 t2   t2_gdpgM t2_gdptM t2_giniM t2_scapM t2_dregM t2_t0  ///
         t3   t3_gdpgM t3_gdptM t3_giniM t3_scapM t3_dregM t3_t0  ///
         || id: t t2 t3
	    est store A61
* For graph 
   mixed libdem $Level1 ($Trend)##($Level2) || id: $Trend 
       est store A61g		

* S62	   
* First stage > Control function
reg gdpg gdpgi  gdpt_   gini_    scap_   dreg_          ///
	            gdptM   giniM    scapM   dregM      t0  /// 
          t   t_gdptM t_giniM  t_scapM t_dregM    t_t0  ///	  
		  t2 t2_gdptM t2_giniM t2_scapM t2_dregM t2_t0  ///
		  t3 t3_gdptM t3_giniM t3_scapM t3_dregM t3_t0 
   predict gdpgcf, residuals
   label var gdpgcf "Control function"	   
		
* Restore original growth values to shell	
   replace gdpg_ = gdpgC   
   replace gdpgM = gdpgM	

* New 2SRI model with control function
   mixed libdem  gdpg_    gdpt_   gini_    scap_   dreg_          ///
                 gdpgM    gdptM   giniM    scapM   dregM      t0  ///
         t     t_gdpgM  t_gdptM t_giniM  t_scapM t_dregM    t_t0  ///
		 t2   t2_gdpgM t2_gdptM t2_giniM t2_scapM t2_dregM t2_t0  ///
         t3   t3_gdpgM t3_gdptM t3_giniM t3_scapM t3_dregM t3_t0  ///
		         gdpgcf  || id: t t2 t3
	    est store A62		
* For graph   
   mixed libdem $Level1 ($Trend)##($Level2) gdpgcf || id: $Trend 
       est store A62g		
		
* Table S6 - 
 esttab M3b A61 A62 ///
      using "TableS6.rtf", ///
	  cell((b(star fmt(%8.2f)) se(par))) wide compress ///
	  star(* 0.05) legend label   ///
	  varwidth(25) modelwidth(7) nomtitles interaction(" ") ///
	  stats ( N , fmt(%9.0g %9.1f) labels("N") )  ///
	  title("Table S6. Growth Curve Model with Instruments") replace ///
	   varlabels( t "Years since transition" _cons "Intercept")	  

	   
 *** Figure S1 - Graphs for latent curve with endogeneity ***
 label drop _all
 label define lgdpgM 1 "1%" 5 "5%"
 label values            gdpgM lgdpgM

 est restore M3
 margins, at(t=(0(2)10)  gdpgM=(1 5)) noestimcheck
 marginsplot, recastci(rarea) recast(line) yscale(r(0(10)100)) ylabel(0(50)100) ///
  ytitle("") title("2.3- Original", size(med)) xsize(6) ysize(3) ///
  legend(region(lcolor(none)))
  graph save "pred3.gph", replace	
 
 est restore A61g
 margins, at(t=(0(2)10)  gdpgM=(1 5)) noestimcheck
 marginsplot, recastci(rarea) recast(line) yscale(r(0(10)100)) ylabel(0(50)100) ///
  ytitle("") title("S6.1- Residual", size(med)) xsize(6) ysize(3) ///
  legend(region(lcolor(none)))
  graph save "predS61.gph", replace	  
  
 est restore A62g
 margins, at(t=(0(2)10)  gdpgM=(1 5)) noestimcheck
 marginsplot, recastci(rarea) recast(line) yscale(r(0(10)100)) ylabel(0(50)100) ///
  ytitle("") title("S6.2- 2SRI", size(med)) xsize(6) ysize(3) ///
  legend(region(lcolor(none)))
  graph save "predS62.gph", replace
  
  global pagesize rows(1) xsize(6) ysize(6)
  
  graph combine "pred3.gph" "predS61.gph" "predS62.gph" ///
				, ycommon $pagesize
  graph export "FigureS1.png", replace width(1000)				