<?php
$tpl_version = "2.6";
if (isset($_GET['ver'])) {
  echo $tpl_version;
  exit;
}
//
// Title    : Webtags converted to PHP Variables
// Plateform: Cumulus v1.9.4 (build 1099)
// Author   : Jacques Desroches (meteoduquebec.com)
// Version  : 2.6 (2015-03-14)
//

// Date formatted
$to = "to ";  // Ex: to 20 may
$pre_time = "at ";  // Ex: at 10:45
$pre_date = ", on ";  // Ex:  on 25 may
$only_date = "On ";  // Ex: On 25 may

// Section  MEASURE UNITS
$tempunit = "degC";
$tempunitnodeg = "C";
$pressunit = "hPa";
$rainunit = "mm";
$windunit = "MPH";
$windrununit = "MILES";
$cloudbaseunit = "ft";

// Section DATE and TIME
$date = "<#date>";
$time = "<#time>";
$timehhmmss = "<#timehhmmss>";
$timeUTC  = "<#timeUTC>";
$day = "<#day>";
$dayname = "<#dayname>";
$shortdayname = "<#shortdayname>";
$month = "<#month>";
$monthname = "<#monthname>";
$shortmonthname = "<#shortmonthname>";
$year = "<#year>";
$shortyear = "<#shortyear>";
$hour = "<#hour>";
$minute = "<#minute>";
$metdate = '<#metdate>';
$metdateyesterday ='<#metdateyesterday>';
$yesterday = '<#yesterday>';
$rollovertime = "<#rollovertime>";
$update = "<#update>";
$LastDataReadT = "<#LastDataReadT>";
$DaysSince30Dec1899 = '<#DaysSince30Dec1899>';
$DaysSinceRecordsBegan = '<#DaysSinceRecordsBegan>';
//-- Section CURRENT CONDITIONS --
$apptemp = "<#apptemp>";
$avgtemp = "<#avgtemp>";
$temp = "21.0";
$intemp = "<#intemp>";
$temptrend = "<#temptrend>";
$temptrendtext = "<#temptrendtext>";
$temptrendenglish = "<#temptrendenglish>";
$TempChangeLastHour = "<#TempChangeLastHour>";
$heatindex = "<#heatindex>";
$humidex = "<#humidex>";
$hum = "<#hum>";
$inhum = "<#inhum>";
$dew = "<#dew>";
$wchill = "<#wchill>";
$wetbulb  = "<#wetbulb>";
$IsFreezing = "<#IsFreezing>";
$rfall = "<#rfall>";
$rrate = "<#rrate>";
$rhour = "<#rhour>";
$rmidnight = "<#rmidnight>";
$r24hour = "<#r24hour>";
$LastRainTipISO = "<#LastRainTipISO>";
$MinutesSinceLastRainTip = "<#MinutesSinceLastRainTip>";
$IsRaining = "<#IsRaining>";
$RG11RainToday = "<#RG11RainToday>";
$press = "<#press>";
$presstrendval = "<#presstrendval>";
$presstrend = "<#presstrend>";
$presstrendenglish = "<#presstrendenglish>";
$altimeterpressure = "<#altimeterpressure>";
$wlatest = "<#wlatest>";
$bearing = "<#bearing>";
$currentwdir = "<#currentwdir>";
$wspeed = "<#wspeed>";
$avgbearing = "<#avgbearing>";
$wdir = "<#wdir>";
$wgust = "<#wgust>";
$wdirdata = "<#wdirdata>";
$wspddata = "<#wdirdata>";
$nextwindindex = "<#nextwindindex>";
$beaufort = "<#beaufort>";
$beaufortnumber = "<#beaufortnumber>";
$beaudesc = "<#beaudesc>";
$BearingRangeFrom = "<#BearingRangeFrom>";
$BearingRangeTo = "<#BearingRangeTo>";
$BearingRangeFrom10 = "<#BearingRangeFrom10>";
$BearingRangeTo10 = "<#BearingRangeTo10>";
$cloudbase = "<#cloudbase>";
$cloudbasevalue = "<#cloudbasevalue>";
$UV = "<#UV>";
$SolarRad = "<#SolarRad>";
$forecast = "<#forecast>";
$forecastenc = "<#forecastenc>";
$forecastnumber = "<#forecastnumber>";
$cumulusforecast = "<#cumulusforecast>";
$cumulusforecastenc = "<#cumulusforecastenc>";
$wsforecast = "<#wsforecast>";
$wsforecastenc = "<#wsforecastenc>";

//-- Section TODAY CONDITIONS --
$tempTH = "<#tempTH>";
$TtempTH = "<#TtempTH>";
$TtempTHF = $pre_time."<#TtempTH>";
$tempTL = "<#tempTL>";
$TtempTL = "<#TtempTL>";
$TtempTLF = $pre_time."<#TtempTL>";
$temprange = "<#temprange>";
$apptempTH = "<#apptempTH>";
$TapptempTH = "<#TapptempTH>";
$TapptempTHF = $pre_time."<#TapptempTH>";
$apptempTL = "<#apptempTL>";
$TapptempTL = "<#TapptempTL>";
$TapptempTLF = $pre_time."<#TapptempTL>";
$heatindexTH = "<#heatindexTH>";
$TheatindexTH = "<#TheatindexTH>";
$TheatindexTHF = $pre_time."<#TheatindexTH>";
$wchillTL = "<#wchillTL>";
$TwchillTL = "<#TwchillTL>";
$TwchillTLF = $pre_time."<#TwchillTL>";
$dewpointTH = "<#dewpointTH>";
$TdewpointTH = "<#TdewpointTH>";
$TdewpointTHF = $pre_time."<#TdewpointTH>";
$dewpointTL = "<#dewpointTL>";
$TdewpointTL = "<#TdewpointTL>";
$TdewpointTLF = $pre_time."<#TdewpointTL>";
$humTH = "<#humTH>";
$ThumTH = "<#ThumTH>";
$ThumTHF = $pre_time."<#ThumTH>";
$humTL = "<#humTL>";
$ThumTL = "<#ThumTL>";
$ThumTLF = $pre_time."<#ThumTL>";
$rrateTM = "<#rrateTM>";
$TrrateTM = "<#TrrateTM>";
$TrrateTMF = $pre_time."<#TrrateTM>";
$hourlyrainTH = "<#hourlyrainTH>";
$ThourlyrainTH = "<#ThourlyrainTH>";
$ThourlyrainTHF = $pre_time."<#ThourlyrainTH>";
$pressTH = "<#pressTH>";
$TpressTH = "<#TpressTH>";
$TpressTHF = $pre_time."<#TpressTH>";
$pressTL = "<#pressTL>";
$TpressTL = "<#TpressTL>";
$TpressTLF = $pre_time."<#TpressTL>";
$windTM = "<#windTM>";
$TwindTM = "<#TwindTM>";
$TwindTMF = $pre_time."<#TwindTM>";
$wgustTM = "<#wgustTM>";
$TwgustTM = "<#TwgustTM>";
$TwgustTMF = $pre_time."<#TwgustTM>";
$bearingTM = "<#bearingTM>";
$Tbeaufort = "<#Tbeaufort>";
$Tbeaufortnumber = "<#Tbeaufortnumber>";
$windrun = "<#windrun>";
$domwindbearing = "<#domwindbearing>";
$domwinddir = "<#domwinddir>";
$Tbeaudesc = "<#Tbeaudesc>";
$ET = "<#ET>";
$heatdegdays = "<#heatdegdays>";
$cooldegdays = "<#cooldegdays>";
$solarTH = "<#solarTH>";
$TsolarTH = "<#TsolarTH>";
$TsolarTHF = $pre_time."<#TsolarTH>";
$UVTH = "<#UVTH>";
$TUVTH = "<#TUVTH>";
$TUVTHF = $pre_time."<#TUVTH>";

//-- Section YESTERDAY CONDITIONS --
$tempYH = "<#tempYH>";
$TtempYH = "<#TtempYH>";
$TtempYHF = $pre_time."<#TtempYH>";
$tempYL = "<#tempYL>";
$TtempYL = "<#TtempYL>";
$TtempYLF = $pre_time."<#TtempYL>";
$avgtempY = "<#avgtempY>";
$temprangeY = "<#temprangeY>";
$apptempYH = "<#apptempYH>";
$TapptempYH = "<#TapptempYH>";
$TapptempYHF = $pre_time."<#TapptempYH>";
$apptempYL = "<#apptempYL>";
$TapptempYL = "<#TapptempYL>";
$TapptempYLF = $pre_time."<#TapptempYL>";
$heatindexYH = "<#heatindexYH>";
$TheatindexYH = "<#TheatindexYH>";
$TheatindexYHF = $pre_time."<#TheatindexYH>";
$wchillYL = "<#wchillYL>";
$TwchillYL = "<#TwchillYL>";
$TwchillYLF = $pre_time."<#TwchillYL>";
$dewpointYH = "<#dewpointYH>";
$TdewpointYH = "<#TdewpointYH>";
$TdewpointYHF = $pre_time."<#TdewpointYH>";
$dewpointYL = "<#dewpointYL>";
$TdewpointYL = "<#TdewpointYL>";
$TdewpointYLF = $pre_time."<#TdewpointYL>";
$humYH = "<#humYH>";
$ThumYH = "<#ThumYH>";
$ThumYHF = $pre_time."<#ThumYH>";
$humYL = "<#humYL>";
$ThumYL = "<#ThumYL>";
$ThumYLF = $pre_time."<#ThumYL>";
$rfallY = "<#rfallY>";
$RG11RainYest = "<#RG11RainYest>";
$rrateYM = "<#rrateYM>";
$TrrateYM = "<#TrrateYM>";
$TrrateYMF = $pre_time."<#TrrateYM>";
$hourlyrainYH = "<#hourlyrainYH>";
$ThourlyrainYH = "<#ThourlyrainYH>";
$ThourlyrainYHF = $pre_time."<#ThourlyrainYH>";
$pressYH = "<#pressYH>";
$TpressYH = "<#TpressYH>";
$TpressYHF = $pre_time."<#TpressYH>";
$pressYL = "<#pressYL>";
$TpressYL = "<#TpressYL>";
$TpressYLF = $pre_time."<#TpressYL>";
$windYM = "<#windYM>";
$TwindYM = "<#TwindYM>";
$TwindYMF = $pre_time."<#TwindYM>";
$wgustYM = "<#wgustYM>";
$TwgustYM = "<#TwgustYM>";
$TwgustYMF = $pre_time."<#TwgustYM>";
$bearingYM = "<#bearingYM>";
$Ybeaufort = "<#Ybeaufort>";
$Ybeaufortnumber = "<#Ybeaufortnumber>";
$Ybeaudesc = "<#Ybeaudesc>";
$domwindbearingY = "<#domwindbearingY>";
$domwinddirY = "<#domwinddirY>";
$windrunY = "<#windrunY>";
$heatdegdaysY = "<#heatdegdaysY>";
$cooldegdaysY = "<#cooldegdaysY>";
$solarYH = "<#solarYH>";
$TsolarYH = "<#TsolarYH>";
$TsolarYHF = $pre_time."<#TsolarYH>";
$UVYH = "<#UVYH>";
$TUVYH = "<#TUVYH>";
$TUVYHF = $pre_time."<#TUVYH>";


//-- Section MONTHLY --
$MonthTempH = "<#MonthTempH>";
$MonthTempHT = "<#MonthTempHT>";
$MonthTempHD = "<#MonthTempHD>";
if (!is_numeric("<#MonthTempHD format='m'>")) $MonthTempHF = "<#MonthTempHD>"; else
$MonthTempHF = $pre_time.$MonthTempHT.$pre_date."<#MonthTempHD format='d'> ".$Tr_monthnames["<#MonthTempHD format='m'>"];
$MonthTempL = "<#MonthTempL>";
$MonthTempLT = "<#MonthTempLT>";
$MonthTempLD = "<#MonthTempLD>";
if (!is_numeric("<#MonthTempLD format='m'>")) $MonthTempLF = "<#MonthTempLD>"; else
$MonthTempLF = $pre_time.$MonthTempLT.$pre_date."<#MonthTempLD format='d'> ".$Tr_monthnames["<#MonthTempLD format='m'>"];
$MonthMinTempH = "<#MonthMinTempH>";
$MonthMinTempHD = "<#MonthMinTempHD>";
if (!is_numeric("<#MonthMinTempHD format='m'>")) $MonthMinTempHF = "<#MonthMinTempHD>"; else
$MonthMinTempHF = $only_date."<#MonthMinTempHD format='d'> ".$Tr_monthnames["<#MonthMinTempHD format='m'>"];
$MonthMaxTempL = "<#MonthMaxTempL>";
$MonthMaxTempLD = "<#MonthMaxTempLD>";
if (!is_numeric("<#MonthMaxTempLD format='m'>")) $MonthMaxTempLF = "<#MonthMaxTempLD>"; else
$MonthMaxTempLF = $only_date."<#MonthMaxTempLD format='d'> ".$Tr_monthnames["<#MonthMaxTempLD format='m'>"];
$MonthHighDailyTempRange = "<#MonthHighDailyTempRange>";
$MonthHighDailyTempRangeD = "<#MonthHighDailyTempRangeD>";
if (!is_numeric("<#MonthHighDailyTempRangeD format='m'>")) $MonthHighDailyTempRangeF = "<#MonthHighDailyTempRangeD>"; else
$MonthHighDailyTempRangeF = $only_date."<#MonthHighDailyTempRangeD format='d'> ".$Tr_monthnames["<#MonthHighDailyTempRangeD format='m'>"];
$MonthLowDailyTempRange = "<#MonthLowDailyTempRange>";
$MonthLowDailyTempRangeD = "<#MonthLowDailyTempRangeD>";
if (!is_numeric("<#MonthLowDailyTempRangeD format='m'>")) $MonthLowDailyTempRangeF = "<#MonthLowDailyTempRangeD>"; else
$MonthLowDailyTempRangeF = $only_date."<#MonthLowDailyTempRangeD format='d'> ".$Tr_monthnames["<#MonthLowDailyTempRangeD format='m'>"];
$MonthHeatIndexH = "<#MonthHeatIndexH>";
$MonthHeatIndexHT = "<#MonthHeatIndexHT>";
$MonthHeatIndexHD = "<#MonthHeatIndexHD>";
if (!is_numeric("<#MonthHeatIndexHD format='m'>")) $MonthHeatIndexHF = "<#MonthHeatIndexHD>"; else
$MonthHeatIndexHF = $pre_time.$MonthHeatIndexHT.$pre_date."<#MonthHeatIndexHD format='d'> ".$Tr_monthnames["<#MonthHeatIndexHD format='m'>"];
$MonthWChillL = "<#MonthWChillL>";
$MonthWChillLT = "<#MonthWChillLT>";
$MonthWChillLD = "<#MonthWChillLD>";
if (!is_numeric("<#MonthWChillLD format='m'>")) $MonthWChillLF = "<#MonthWChillLD>";
$MonthWChillLF = $pre_time.$MonthWChillLT.$pre_date."<#MonthWChillLD format='d'> ".$Tr_monthnames["<#MonthWChillLD format='m'>"];
$MonthAppTempH = "<#MonthAppTempH>";
$MonthAppTempHT = "<#MonthAppTempHT>";
$MonthAppTempHD = "<#MonthAppTempHD>";
if (!is_numeric("<#MonthAppTempHD format='m'>")) $MonthAppTempHF = "<#MonthAppTempHD>"; else
$MonthAppTempHF = $pre_time.$MonthAppTempHT.$pre_date."<#MonthAppTempHD format='d'> ".$Tr_monthnames["<#MonthAppTempHD format='m'>"];
$MonthAppTempL = "<#MonthAppTempL>";
$MonthAppTempLT = "<#MonthAppTempLT>";
$MonthAppTempLD = "<#MonthAppTempLD>";
if (!is_numeric("<#MonthAppTempLD format='m'>")) $MonthAppTempLF = "<#MonthAppTempLD>"; else
$MonthAppTempLF = $pre_time.$MonthAppTempLT.$pre_date."<#MonthAppTempLD format='d'> ".$Tr_monthnames["<#MonthAppTempLD format='m'>"];
$MonthDewPointH = "<#MonthDewPointH>";
$MonthDewPointHT = "<#MonthDewPointHT>";
$MonthDewPointHD = "<#MonthDewPointHD>";
if (!is_numeric("<#MonthDewPointHD format='m'>")) $MonthDewPointHF = "<#MonthDewPointHD>"; else
$MonthDewPointHF = $pre_time.$MonthDewPointHT.$pre_date."<#MonthDewPointHD format='d'> ".$Tr_monthnames["<#MonthDewPointHD format='m'>"];
$MonthDewPointL = "<#MonthDewPointL>";
$MonthDewPointLT = "<#MonthDewPointLT>";
$MonthDewPointLD = "<#MonthDewPointLD>";
if (!is_numeric("<#MonthDewPointLD format='m'>")) $MonthDewPointLF = "<#MonthDewPointLD>"; else
$MonthDewPointLF = $pre_time.$MonthDewPointLT.$pre_date."<#MonthDewPointLD format='d'> ".$Tr_monthnames["<#MonthDewPointLD format='m'>"];
$MonthHumH = "<#MonthHumH>";
$MonthHumHT = "<#MonthHumHT>";
$MonthHumHD = "<#MonthHumHD>";
if (!is_numeric("<#MonthHumHD format='m'>")) $MonthHumHF = "<#MonthHumHD>"; else
$MonthHumHF = $pre_time.$MonthHumHT.$pre_date."<#MonthHumHD format='d'> ".$Tr_monthnames["<#MonthHumHD format='m'>"];
$MonthHumL = "<#MonthHumL>";
$MonthHumLT = "<#MonthHumLT>";
$MonthHumLD = "<#MonthHumLD>";
if (!is_numeric("<#MonthHumLD format='m'>")) $MonthHumLF = "<#MonthHumLD>"; else
$MonthHumLF = $pre_time.$MonthHumLT.$pre_date."<#MonthHumLD format='d'> ".$Tr_monthnames["<#MonthHumLD format='m'>"];
$MonthPressH = "<#MonthPressH>";
$MonthPressHT = "<#MonthPressHT>";
$MonthPressHD = "<#MonthPressHD>";
if (!is_numeric("<#MonthPressHD format='m'>")) $MonthPressHF = "<#MonthPressHD>"; else
$MonthPressHF = $pre_time.$MonthPressHT.$pre_date."<#MonthPressHD format='d'> ".$Tr_monthnames["<#MonthPressHD format='m'>"];
$MonthPressL = "<#MonthPressL>";
$MonthPressLT = "<#MonthPressLT>";
$MonthPressLD = "<#MonthPressLD>";
if (!is_numeric("<#MonthPressLD format='m'>")) $MonthPressLF = "<#MonthPressLD>"; else
$MonthPressLF = $pre_time.$MonthPressLT.$pre_date."<#MonthPressLD format='d'> ".$Tr_monthnames["<#MonthPressLD format='m'>"];
$MonthGustH = "<#MonthGustH>";
$MonthGustHT = "<#MonthGustHT>";
$MonthGustHD = "<#MonthGustHD>";
if (!is_numeric("<#MonthGustHD format='m'>")) $MonthGustHF = "<#MonthGustHD>"; else
$MonthGustHF = $pre_time.$MonthGustHT.$pre_date."<#MonthGustHD format='d'> ".$Tr_monthnames["<#MonthGustHD format='m'>"];
$MonthWindH = "<#MonthWindH>";
$MonthWindHT = "<#MonthWindHT>";
$MonthWindHD = "<#MonthWindHD>";
if (!is_numeric("<#MonthWindHD format='m'>")) $MonthWindHF = "<#MonthWindHD>"; else
$MonthWindHF = $pre_time.$MonthWindHT.$pre_date."<#MonthWindHD format='d'> ".$Tr_monthnames["<#MonthWindHD format='m'>"];
$MonthWindRunH = "<#MonthWindRunH>";
$MonthWindRunHD = "<#MonthWindRunHD>";
if (!is_numeric("<#MonthWindRunHD format='m'>")) $MonthWindRunHF = "<#MonthWindRunHD>"; else
$MonthWindRunHF = $only_date."<#MonthWindRunHD format='d'> ".$Tr_monthnames["<#MonthWindRunHD format='m'>"];
$rmonth = "<#rmonth>";
$MonthRainRateH = "<#MonthRainRateH>";
$MonthRainRateHT = "<#MonthRainRateHT>";
$MonthRainRateHD = "<#MonthRainRateHD>";
if (!is_numeric("<#MonthRainRateHD format='m'>")) $MonthRainRateHF = "<#MonthRainRateHD>"; else
$MonthRainRateHF = $pre_time.$MonthRainRateHT.$pre_date."<#MonthRainRateHD format='d'> ".$Tr_monthnames["<#MonthRainRateHD format='m'>"];
$MonthHourlyRainH = "<#MonthHourlyRainH>";
$MonthHourlyRainHT = "<#MonthHourlyRainHT>";
$MonthHourlyRainHD = "<#MonthHourlyRainHD>";
if (!is_numeric("<#MonthHourlyRainHD format='m'>")) $MonthHourlyRainHF = "<#MonthHourlyRainHD>"; else
$MonthHourlyRainHF = $pre_time.$MonthHourlyRainHT.$pre_date."<#MonthHourlyRainHD format='d'> ".$Tr_monthnames["<#MonthHourlyRainHD format='m'>"];
$MonthDailyRainH = "<#MonthDailyRainH>";
$MonthDailyRainHD = "<#MonthDailyRainHD>";
if (!is_numeric("<#MonthDailyRainHD format='m'>")) $MonthDailyRainHF = "<#MonthDailyRainHD>"; else
$MonthDailyRainHF = $only_date."<#MonthDailyRainHD format='d'> ".$Tr_monthnames["<#MonthDailyRainHD format='m'>"];
$MonthLongestDryPeriod = "<#MonthLongestDryPeriod>";
$MonthLongestDryPeriodD = "<#MonthLongestDryPeriodD>";
if (!is_numeric("<#MonthLongestDryPeriodD format='m'>")) $MonthLongestDryPeriodF = "<#MonthLongestDryPeriodD>"; else
$MonthLongestDryPeriodF = $to."<#MonthLongestDryPeriodD format='d'> ".$Tr_monthnames["<#MonthLongestDryPeriodD format='m'>"];
$MonthLongestWetPeriod = "<#MonthLongestWetPeriod>";
$MonthLongestWetPeriodD = "<#MonthLongestWetPeriodD>";
if (!is_numeric("<#MonthLongestWetPeriodD format='m'>")) $MonthLongestWetPeriodF = "<#MonthLongestWetPeriodD>"; else
$MonthLongestWetPeriodF = $to."<#MonthLongestWetPeriodD format='d'> ".$Tr_monthnames["<#MonthLongestWetPeriodD format='m'>"];

//-- Section ANNUAL --
$YearTempH = "<#YearTempH>";
$YearTempHT = "<#YearTempHT>";
$YearTempHD = "<#YearTempHD>";
if (!is_numeric("<#YearTempHD format='m'>")) $YearTempHF = $YearTempHD; else
$YearTempHF = $pre_time.$YearTempHT.$pre_date."<#YearTempHD format='d'> ".$Tr_monthnames["<#YearTempHD format='m'>"];;
$YearTempL = "<#YearTempL>";
$YearTempLT = "<#YearTempLT>";
$YearTempLD = "<#YearTempLD>";
if (!is_numeric("<#YearTempLD format='m'>")) $YearTempLF = $YearTempLD; else
$YearTempLF = $pre_time.$YearTempLT.$pre_date."<#YearTempLD format='d'> ".$Tr_monthnames["<#YearTempLD format='m'>"];;
$YearHighDailyTempRange = "<#YearHighDailyTempRange>";
$YearHighDailyTempRangeD = "<#YearHighDailyTempRangeD>";
if (!is_numeric("<#YearHighDailyTempRangeD format='m'>")) $YearHighDailyTempRangeF = $YearHighDailyTempRangeD; else
$YearHighDailyTempRangeF = $only_date."<#YearHighDailyTempRangeD format='d'> ".$Tr_monthnames["<#YearHighDailyTempRangeD format='m'>"];;
$YearLowDailyTempRange = "<#YearLowDailyTempRange>";
$YearLowDailyTempRangeD = "<#YearLowDailyTempRangeD>";
if (!is_numeric("<#YearLowDailyTempRangeD format='m'>")) $YearLowDailyTempRangeF = $YearLowDailyTempRangeD; else
$YearLowDailyTempRangeF = $only_date."<#YearLowDailyTempRangeD format='d'> ".$Tr_monthnames["<#YearLowDailyTempRangeD format='m'>"];;
$YearHeatIndexH = "<#YearHeatIndexH>";
$YearHeatIndexHT = "<#YearHeatIndexHT>";
$YearHeatIndexHD = "<#YearHeatIndexHD>";
if (!is_numeric("<#YearHeatIndexHD format='m'>")) $YearHeatIndexHF = $YearHeatIndexHD; else
$YearHeatIndexHF = $pre_time.$YearHeatIndexHT.$pre_date."<#YearHeatIndexHD format='d'> ".$Tr_monthnames["<#YearHeatIndexHD format='m'>"];;
$YearWChillL = "<#YearWChillL>";
$YearWChillLT = "<#YearWChillLT>";
$YearWChillLD = "<#YearWChillLD>";
if (!is_numeric("<#YearWChillLD format='m'>")) $YearWChillLF = $YearWChillLD; else
$YearWChillLF = $pre_time.$YearWChillLT.$pre_date."<#YearWChillLD format='d'> ".$Tr_monthnames["<#YearWChillLD format='m'>"];;
$YearAppTempH = "<#YearAppTempH>";
$YearAppTempHT = "<#YearAppTempHT>";
$YearAppTempHD = "<#YearAppTempHD>";
if (!is_numeric("<#YearAppTempHD format='m'>")) $YearAppTempHF = $YearAppTempHD; else
$YearAppTempHF = $pre_time.$YearAppTempHT.$pre_date."<#YearAppTempHD format='d'> ".$Tr_monthnames["<#YearAppTempHD format='m'>"];
$YearAppTempL = "<#YearAppTempL>";
$YearAppTempLT = "<#YearAppTempLT>";
$YearAppTempLD = "<#YearAppTempLD>";
if (!is_numeric("<#YearAppTempLD format='m'>")) $YearAppTempLF = $YearAppTempLD; else
$YearAppTempLF = $pre_time.$YearAppTempLT.$pre_date."<#YearAppTempLD format='d'> ".$Tr_monthnames["<#YearAppTempLD format='m'>"];
$YearDewPointH = "<#YearDewPointH>";
$YearDewPointHT = "<#YearDewPointHT>";
$YearDewPointHD = "<#YearDewPointHD>";
if (!is_numeric("<#YearDewPointHD format='m'>")) $YearDewPointHF = $YearDewPointHD; else
$YearDewPointHF = $pre_time.$YearDewPointHT.$pre_date."<#YearDewPointHD format='d'> ".$Tr_monthnames["<#YearDewPointHD format='m'>"];
$YearDewPointL = "<#YearDewPointL>";
$YearDewPointLT = "<#YearDewPointLT>";
$YearDewPointLD = "<#YearDewPointLD>";
if (!is_numeric("<#YearDewPointLD format='m'>")) $YearDewPointLF = $YearDewPointLD; else
$YearDewPointLF = $pre_time.$YearDewPointLT.$pre_date."<#YearDewPointLD format='d'> ".$Tr_monthnames["<#YearDewPointLD format='m'>"];
$YearMinTempH = "<#YearMinTempH>";
$YearMinTempHD = "<#YearMinTempHD>";
if (!is_numeric("<#YearMinTempHD format='m'>")) $YearMinTempHF = $YearMinTempHD;else 
$YearMinTempHF = $only_date."<#YearMinTempHD format='d'> ".$Tr_monthnames["<#YearMinTempHD format='m'>"];
$YearMaxTempL = "<#YearMaxTempL>";
$YearMaxTempLD = "<#YearMaxTempLD>";
if (!is_numeric("<#YearMaxTempLD format='m'>")) $YearMaxTempLF = $YearMaxTempLD; else
$YearMaxTempLF = $only_date."<#YearMaxTempLD format='d'> ".$Tr_monthnames["<#YearMaxTempLD format='m'>"];
$YearHumH = "<#YearHumH>";
$YearHumHT = "<#YearHumHT>";
$YearHumHD = "<#YearHumHD>";
if (!is_numeric("<#YearHumHD format='m'>")) $YearHumHF = $YearHumHD;else
$YearHumHF = $pre_time.$YearHumHT.$pre_date."<#YearHumHD format='d'> ".$Tr_monthnames["<#YearHumHD format='m'>"];
$YearHumL = "<#YearHumL>";
$YearHumLT = "<#YearHumLT>";
$YearHumLD = "<#YearHumLD>";
if (!is_numeric("<#YearHumLD format='m'>")) $YearHumLF = $YearHumLD; else
$YearHumLF = $pre_time.$YearHumLT.$pre_date."<#YearHumLD format='d'> ".$Tr_monthnames["<#YearHumLD format='m'>"];
$YearPressH = "<#YearPressH>";
$YearPressHT = "<#YearPressHT>";
$YearPressHD = "<#YearPressHD>";
if (!is_numeric("<#YearPressHD format='m'>")) $YearPressHF = $YearPressHD; else
$YearPressHF = $pre_time.$YearPressHT.$pre_date."<#YearPressHD format='d'> ".$Tr_monthnames["<#YearPressHD format='m'>"];
$YearPressL = "<#YearPressL>";
$YearPressLT = "<#YearPressLT>";
$YearPressLD = "<#YearPressLD>";
if (!is_numeric("<#YearPressLD format='m'>")) $YearPressLF = $YearPressLD; else
$YearPressLF = $pre_time.$YearPressLT.$pre_date."<#YearPressLD format='d'> ".$Tr_monthnames["<#YearPressLD format='m'>"];
$YearGustH = "<#YearGustH>";
$YearGustHT = "<#YearGustHT>";
$YearGustHD = "<#YearGustHD>";
if (!is_numeric("<#YearGustHD format='m'>")) $YearGustHF = $YearGustHD; else
$YearGustHF = $pre_time.$YearGustHT.$pre_date."<#YearGustHD format='d'> ".$Tr_monthnames["<#YearGustHD format='m'>"];
$YearWindH = "<#YearWindH>";
$YearWindHT = "<#YearWindHT>";
$YearWindHD = "<#YearWindHD>";
if (!is_numeric("<#YearWindHD format='m'>")) $YearWindHF = $YearWindHD; else
$YearWindHF = $pre_time.$YearWindHT.$pre_date."<#YearWindHD format='d'> ".$Tr_monthnames["<#YearWindHD format='m'>"];
$YearWindRunH = "<#YearWindRunH>";
$YearWindRunHD = "<#YearWindRunHD>";
if (!is_numeric("<#YearWindRunHD format='m'>")) $YearWindRunHF = $YearWindRunHD; else
$YearWindRunHF = $only_date."<#YearWindRunHD format='d'> ".$Tr_monthnames["<#YearWindRunHD format='m'>"];
$ryear = "<#ryear>";
$YearRainRateH = "<#YearRainRateH>";
$YearRainRateHT = "<#YearRainRateHT>";
$YearRainRateHD = "<#YearRainRateHD>";
if (!is_numeric("<#YearRainRateHD format='m'>")) $YearRainRateHF = $YearRainRateHD; else
$YearRainRateHF = $pre_time.$YearRainRateHT.$pre_date."<#YearRainRateHD format='d'> ".$Tr_monthnames["<#YearRainRateHD format='m'>"];
$YearHourlyRainH = "<#YearHourlyRainH>";
$YearHourlyRainHT = "<#YearHourlyRainHT>";
$YearHourlyRainHD = "<#YearHourlyRainHD>";
if (!is_numeric("<#YearHourlyRainHD format='m'>")) $YearHourlyRainHF = $YearHourlyRainHD; else
$YearHourlyRainHF = $pre_time.$YearHourlyRainHT.$pre_date."<#YearHourlyRainHD format='d'> ".$Tr_monthnames["<#YearHourlyRainHD format='m'>"];
$YearDailyRainH = "<#YearDailyRainH>";
$YearDailyRainHD = "<#YearDailyRainHD>";
if (!is_numeric("<#YearDailyRainHD format='m'>")) $YearDailyRainHF = $YearDailyRainHD; else
$YearDailyRainHF = $only_date."<#YearDailyRainHD format='d'> ".$Tr_monthnames["<#YearDailyRainHD format='m'>"];
$YearMonthlyRainH = "<#YearMonthlyRainH>";
$YearMonthlyRainHD = "<#YearMonthlyRainHD>";
if (!is_numeric("<#YearMonthlyRainHD format='m'>")) $YearMonthlyRainHF = $YearMonthlyRainHD; else
$YearMonthlyRainHF = $Tr_monthnames["<#YearMonthlyRainHD format='m'>"];
$YearLongestDryPeriod = "<#YearLongestDryPeriod>";
$YearLongestDryPeriodD = "<#YearLongestDryPeriodD>";
if (!is_numeric("<#YearLongestDryPeriodD format='m'>")) $YearLongestDryPeriodF = $YearLongestDryPeriodD; else
$YearLongestDryPeriodF = $to."<#YearLongestDryPeriodD format='d'> ".$Tr_monthnames["<#YearLongestDryPeriodD format='m'>"];
$YearLongestWetPeriod = "<#YearLongestWetPeriod>";
$YearLongestWetPeriodD = "<#YearLongestWetPeriodD>";
if (!is_numeric("<#YearLongestWetPeriodD format='m'>")) $YearLongestWetPeriodF = $YearLongestWetPeriodD; else
$YearLongestWetPeriodF = $to."<#YearLongestWetPeriodD format='d'> ".$Tr_monthnames["<#YearLongestWetPeriodD format='m'>"];

//-- Section All Time RECORDS --
$tempH = "<#tempH>";
$TtempH = "<#TtempH>";
$TtempHF = $pre_time.'<#TtempH format="h'h'nn">'.$pre_date.'<#TtempH format="d ">'.$Tr_monthnames['<#TtempH format="m">'].'<#TtempH format=" yyyy">';
$tempL = "<#tempL>";
$TtempL = "<#TtempL>";
$TtempLF = $pre_time.'<#TtempL format="h'h'nn">'.$pre_date.'<#TtempL format="d ">'.$Tr_monthnames['<#TtempL format="m">'].'<#TtempL format=" yyyy">';
$mintempH = "<#mintempH>";
$TmintempH = "<#TmintempH>";
$TmintempHF = $pre_time.'<#TmintempH format="h'h'nn">'.$pre_date.'<#TmintempH format="d ">'.$Tr_monthnames['<#TmintempH format="m">'].'<#TmintempH format=" yyyy">';
$maxtempL = "<#maxtempL>";
$TmaxtempL = "<#TmaxtempL>";
$TmaxtempLF = $pre_time.'<#TmaxtempL format="h'h'nn">'.$pre_date.'<#TmaxtempL format="d ">'.$Tr_monthnames['<#TmaxtempL format="m">'].'<#TmaxtempL format=" yyyy">';
$LowDailyTempRange = "<#LowDailyTempRange>";
$LowDailyTempRangeD = "<#TLowDailyTempRange>";
$LowDailyTempRangeDF = $only_date.'<#TLowDailyTempRange format="d ">'.$Tr_monthnames['<#TLowDailyTempRange format="m">'].'<#TLowDailyTempRange format=" yyyy">';
$HighDailyTempRange = "<#HighDailyTempRange>";
$HighDailyTempRangeD = "<#THighDailyTempRange>";
$HighDailyTempRangeDF = $only_date.'<#THighDailyTempRange format="d ">'.$Tr_monthnames['<#THighDailyTempRange format="m">'].'<#THighDailyTempRange format=" yyyy">';
$apptempH = "<#apptempH>";
$TapptempH = "<#TapptempH>";
$TapptempHF = $pre_time.'<#TapptempH format="h'h'nn">'.$pre_date.'<#TapptempH format="d ">'.$Tr_monthnames['<#TapptempH format="m">'].'<#TapptempH format=" yyyy">';
$apptempL = "<#apptempL>";
$TapptempL = "<#TapptempL>";
$TapptempLF = $pre_time.'<#TapptempL format="h'h'nn">'.$pre_date.'<#TapptempL format="d ">'.$Tr_monthnames['<#TapptempL format="m">'].'<#TapptempL format=" yyyy">';
$heatindexH = "<#heatindexH>";
$TheatindexH = "<#TheatindexH>";
$TheatindexHF = $pre_time.'<#TheatindexH format="h'h'nn">'.$pre_date.'<#TheatindexH format="d ">'.$Tr_monthnames['<#TheatindexH format="m">'].'<#TheatindexH format=" yyyy">';
$dewpointH = "<#dewpointH>";
$TdewpointH = "<#TdewpointH>";
$TdewpointHF = $pre_time.'<#TdewpointH format="h'h'nn">'.$pre_date.'<#TdewpointH format="d ">'.$Tr_monthnames['<#TdewpointH format="m">'].'<#TdewpointH format=" yyyy">';
$dewpointL = "<#dewpointL>";
$TdewpointL = "<#TdewpointL>";
$TdewpointLF = $pre_time.'<#TdewpointL format="h'h'nn">'.$pre_date.'<#TdewpointL format="d ">'.$Tr_monthnames['<#TdewpointL format="m">'].'<#TdewpointL format=" yyyy">';
$humH = "<#humH>";
$ThumH = "<#ThumH>";
$ThumHF = $pre_time.'<#ThumH format="h'h'nn">'.$pre_date.'<#ThumH format="d ">'.$Tr_monthnames['<#ThumH format="m">'].'<#ThumH format=" yyyy">';
$humL = "<#humL>";
$ThumL = "<#ThumL>";
$ThumLF = $pre_time.'<#ThumL format="h'h'nn">'.$pre_date.'<#ThumL format="d ">'.$Tr_monthnames['<#ThumL format="m">'].'<#ThumL format=" yyyy">';
$wchillH = "<#wchillH>";
$TwchillH = "<#TwchillH>";
$TwchillHF = $pre_time.'<#TwchillH format="h'h'nn">'.$pre_date.'<#TwchillH format="d ">'.$Tr_monthnames['<#TwchillH format="m">'].'<#TwchillH format=" yyyy">';
$rrateM = "<#rrateM>";
$TrrateM = "<#TrrateM>";
$TrrateMF = $pre_time.'<#TrrateM format="h'h'nn">'.$pre_date.'<#TrrateM format="d ">'.$Tr_monthnames['<#TrrateM format="m">'].'<#TrrateM format=" yyyy">';
$rfallH = "<#rfallH>";
$TrfallH = "<#TrfallH>";
$TrfallHF = $only_date.'<#TrfallH format="d ">'.$Tr_monthnames['<#TrfallH format="m">'].'<#TrfallH format=" yyyy">';
$rfallhH = "<#rfallhH>";
$TrfallhH = "<#TrfallhH>";
$TrfallhHF = $pre_time.'<#TrfallhH format="h'h'nn">'.$pre_date.'<#TrfallhH format="d ">'.$Tr_monthnames['<#TrfallhH format="m">'].'<#TrfallhH format=" yyyy">';
$rfallmH = "<#rfallmH>";
$TrfallmH = "<#TrfallmH>";
$TrfallmHF = $pre_time.'<#TrfallmH format="h'h'nn">'.$pre_date.'<#TrfallmH format="d ">'.$Tr_monthnames['<#TrfallmH format="m">'].'<#TrfallmH format=" yyyy">';
$LongestDryPeriod = "<#LongestDryPeriod>";
$TLongestDryPeriod = "<#TLongestDryPeriod>";
$TLongestDryPeriodF = $to.'<#TLongestDryPeriod format="d ">'.$Tr_monthnames['<#TLongestDryPeriod format="m">'].'<#TLongestDryPeriod format=" yyyy">';
$LongestWetPeriod = "<#LongestWetPeriod>";
$TLongestWetPeriod = "<#TLongestWetPeriod>";
$TLongestWetPeriodF = $to.'<#TLongestWetPeriod format="d ">'.$Tr_monthnames['<#TLongestWetPeriod format="m">'].'<#TLongestWetPeriod format=" yyyy">';
$pressH = "<#pressH>";
$TpressH = "<#TpressH>";
$TpressHF = $pre_time.'<#TpressH format="h'h'nn">'.$pre_date.'<#TpressH format="d ">'.$Tr_monthnames['<#TpressH format="m">'].'<#TpressH format=" yyyy">';
$pressL = "<#pressL>";
$TpressL = "<#TpressL>";
$TpressLF = $pre_time.'<#TpressL format="h'h'nn">'.$pre_date.'<#TpressL format="d ">'.$Tr_monthnames['<#TpressL format="m">'].'<#TpressL format=" yyyy">';
$gustM = "<#gustM>";
$TgustM = "<#TgustM>";
$TgustMF = $pre_time.'<#TgustM format="h'h'nn">'.$pre_date.'<#TgustM format="d ">'.$Tr_monthnames['<#TgustM format="m">'].'<#TgustM format=" yyyy">';
$wspeedH = "<#wspeedH>";
$TwspeedH = "<#TwspeedH>";
$TwspeedHF = $pre_time.'<#TwspeedH format="h'h'nn">'.$pre_date.'<#TwspeedH format="d ">'.$Tr_monthnames['<#TwspeedH format="m">'].'<#TwspeedH format=" yyyy">';
$windrunH = "<#windrunH>";
$TwindrunH = "<#TwindrunH>";
$TwindrunHF = $only_date.'<#TwindrunH format="d ">'.$Tr_monthnames['<#TwindrunH format="m">'].'<#TwindrunH format=" yyyy">';

//-- Section Recent History --
$RecentTS = "<#RecentTS>";
$RecentOutsideTemp = "<#RecentOutsideTemp>";
$RecentWindSpeed = "<#RecentWindSpeed>";
$RecentWindGust = "<#RecentWindGust>";
$RecentWindLatest = "<#RecentWindLatest>";
$RecentWindDir = "<#RecentWindDir>";
$RecentWindAvgDir = "<#RecentWindAvgDir>";
$RecentWindChill = "<#RecentWindChill>";
$RecentDewPoint = "<#RecentDewPoint>";
$RecentHeatIndex = "<#RecentHeatIndex>";
$RecentHumidity = "<#RecentHumidity>";
$RecentPressure = "<#RecentPressure>";
$RecentRainToday = "<#RecentRainToday>";
$RecentSolarRad = "<#RecentSolarRad>";
$RecentUV = "<#RecentUV>";

//-- Section OTHERS --
$LatestError = "<#LatestError>";
$LatestErrorDate = "<#LatestErrorDate>";
$LatestErrorTime = "<#LatestErrorTime>";
$ErrorLight = "<#ErrorLight>";
$version = "<#version>";
$build = "<#build>";
$realtimeinterval = "<#realtimeinterval>";
$interval = "<#interval>";
$stationtype = "<#stationtype>";
$latitude = "<#latitude>";
$latitudeD = "<#latitude dp=5 rc=y>";
$longitude = "<#longitude>";
$longitudeD = "<#longitude dp=5 rc=y>";
$altitude = "<#altitude>";
$location = "<#location>";
$longlocation = "<#longlocation>";
$forum = '<#forum>';
$webcam = '<#webcam>';
$graphperiod = "<#graphperiod>";
$snowdepth = "<#snowdepth>";
$currcond = "<#currcond>";
$currcondenc = "<#currcondenc>";
$chillhours = "<#chillhours>";
$ConsecutiveRainDays = "<#ConsecutiveRainDays>";
$ConsecutiveDryDays = "<#ConsecutiveDryDays>";
$WindRoseData = "<#WindRoseData>";
$WindRosePoints = "<#WindRosePoints>";
$WindSampleCount = "<#WindSampleCount>";
$LatestNOAAMonthlyReport = "<#LatestNOAAMonthlyReport>";
$LatestNOAAYearlyReport = "<#LatestNOAAYearlyReport>";

//-- Section DAY, NIGHT, SUN and MOON --
$sunrise = "<#sunrise>";
$sunset = "<#sunset>";
$daylength = "<#daylength>";
$IsSunUp = "<#IsSunUp>";
$dawn = "<#dawn>";
$dusk = "<#dusk>";
$daylightlength = "<#daylightlength>";
$isdaylight = "<#isdaylight>";
$tomorrowdaylength = "<#tomorrowdaylength>";
$moonphase = "<#moonphase>";
$MoonAge = "<#MoonAge>";
$moonrise = "<#moonrise>";
$moonset = "<#moonset>";
$MoonPercent = "<#MoonPercent>";
$MoonPercentAbs = "<#MoonPercentAbs>";
$SunshineHours = "<#SunshineHours>";
$YSunshineHours = "<#YSunshineHours>";
$CurrentSolarMax = "<#CurrentSolarMax>";
$IsSunny = "<#IsSunny>";
	
//-- Section ALARMS --
$LowTempAlarm = "<#LowTempAlarm>";
$HighTempAlarm = "<#HighTempAlarm>";
$TempChangeUpAlarm = "<#TempChangeUpAlarm>";
$TempChangeDownAlarm = "<#TempChangeDownAlarm>";
$LowPressAlarm = "<#LowPressAlarm>";
$HighPressAlarm = "<#HighPressAlarm>";
$PressChangeUpAlarm = "<#PressChangeUpAlarm>";
$PressChangeDownAlarm = "<#PressChangeDownAlarm>";
$HighRainTodayAlarm = "<#HighRainTodayAlarm>";
$HighRainRateAlarm = "<#HighRainRateAlarm>";
$HighWindGustAlarm = "<#HighWindGustAlarm>";
$HighWindSpeedAlarm = "<#HighWindSpeedAlarm>";
$DataStopped = "<#DataStopped>";

//-- Section RECORDS INDICATORS --
$recordsbegandate = "<#recordsbegandate>";
$newrecord = "<#newrecord>";
$TempRecordSet = "<#TempRecordSet>";
$WindRecordSet = "<#WindRecordSet>";
$RainRecordSet = "<#RainRecordSet>";
$HumidityRecordSet = "<#HumidityRecordSet>";
$PressureRecordSet = "<#PressureRecordSet>";
$HighTempRecordSet = "<#HighTempRecordSet>";
$LowTempRecordSet = "<#LowTempRecordSet>";
$HighTempRangeRecordSet = "<#HighTempRangeRecordSet>";
$LowTempRangeRecordSet = "<#LowTempRangeRecordSet>";
$HighAppTempRecordSet = "<#HighAppTempRecordSet>";
$LowAppTempRecordSet = "<#LowAppTempRecordSet>";
$HighHeatIndexRecordSet = "<#HighHeatIndexRecordSet>";
$LowWindChillRecordSet = "<#LowWindChillRecordSet>";
$HighDewPointRecordSet = "<#HighDewPointRecordSet>";
$LowDewPointRecordSet = "<#LowDewPointRecordSet>";
$HighMinTempRecordSet = "<#HighMinTempRecordSet>";
$LowMaxTempRecordSet = "<#LowMaxTempRecordSet>";
$HighWindGustRecordSet = "<#HighWindGustRecordSet>";
$HighWindSpeedRecordSet = "<#HighWindSpeedRecordSet>";
$HighRainRateRecordSet = "<#HighRainRateRecordSet>";
$HighHourlyRainRecordSet = "<#HighHourlyRainRecordSet>";
$HighDailyRainRecordSet = "<#HighDailyRainRecordSet>";
$HighMonthlyRainRecordSet = "<#HighMonthlyRainRecordSet>";
$LongestDryPeriodRecordSet = "<#LongestDryPeriodRecordSet>";
$LongestWetPeriodRecordSet = "<#LongestWetPeriodRecordSet>";
$HighHumidityRecordSet = "<#HighHumidityRecordSet>";
$LowHumidityRecordSet = "<#LowHumidityRecordSet>";
$HighPressureRecordSet = "<#HighPressureRecordSet>";
$LowPressureRecordSet = "<#LowPressureRecordSet>";
$HighWindrunRecordSet = "<#HighWindrunRecordSet>";
	
//-- Section WEBTAGS SPECIAL --
$ExtraTemp1 = "<#ExtraTemp1>";
$ExtraTemp2 = "<#ExtraTemp2>";
$ExtraTemp3 = "<#ExtraTemp3>";
$ExtraTemp4 = "<#ExtraTemp4>";
$ExtraTemp5 = "<#ExtraTemp5>";
$ExtraTemp6 = "<#ExtraTemp6>";
$ExtraTemp7 = "<#ExtraTemp7>";
$ExtraTemp8 = "<#ExtraTemp8>";
$ExtraTemp9 = "<#ExtraTemp9>";
$ExtraTemp10 = "<#ExtraTemp10>";
$ExtraDP1 = "<#ExtraDP1>";
$ExtraDP2 = "<#ExtraDP2>";
$ExtraDP3 = "<#ExtraDP3>";
$ExtraDP4 = "<#ExtraDP4>";
$ExtraDP5 = "<#ExtraDP5>";
$ExtraDP6 = "<#ExtraDP6>";
$ExtraDP7 = "<#ExtraDP7>";
$ExtraDP8 = "<#ExtraDP8>";
$ExtraDP9 = "<#ExtraDP9>";
$ExtraDP10 = "<#ExtraDP10>";
$ExtraHum1 = "<#ExtraHum1>";
$ExtraHum2 = "<#ExtraHum2>";
$ExtraHum3 = "<#ExtraHum2>";
$ExtraHum4 = "<#ExtraHum4>";
$ExtraHum5 = "<#ExtraHum5>";
$ExtraHum6 = "<#ExtraHum6>";
$ExtraHum7 = "<#ExtraHum7>";
$ExtraHum8 = "<#ExtraHum8>";
$ExtraHum9 = "<#ExtraHum9>";
$ExtraHum10 = "<#ExtraHum10>";
$SoilTemp1 = "<#SoilTemp1>";
$SoilTemp2 = "<#SoilTemp2>";
$SoilTemp3 = "<#SoilTemp3>";
$SoilTemp4 = "<#SoilTemp4>";
$SoilMoisture1 = "<#SoilMoisture1>";
$SoilMoisture2 = "<#SoilMoisture2>";
$SoilMoisture3 = "<#SoilMoisture3>";
$SoilMoisture4 = "<#SoilMoisture4>";
$LeafTemp1 = "<#LeafTemp1>";
$LeafTemp2 = "<#LeafTemp2>";
$LeafWetness1 = "<#LeafWetness1>";
$LeafWetness2 = "<#LeafWetness2>";
	
//-- Section DAVIS  --
$DavisTotalPacketsReceived = "<#DavisTotalPacketsReceived>";
$DavisTotalPacketsMissed = "<#DavisTotalPacketsMissed>";
$DavisNumberOfResynchs = "<#DavisNumberOfResynchs>";
$DavisMaxInARow = "<#DavisMaxInARow>";
$DavisNumCRCerrors = "<#DavisNumCRCerrors>";
$THWindex = "<#THWindex>";
$THSWindex = "<#THSWindex>";
$DavisFirmwareVersion = "<#DavisFirmwareVersion>";
$battery = "<#battery>";
$txbattery = "<#txbattery>";
$txbattery1 = "<#txbattery channel=1>";		
$txbattery2 = "<#txbattery channel=2>";		
$txbattery3 = "<#txbattery channel=3>";		
$txbattery4 = "<#txbattery channel=4>";		
$txbattery5 = "<#txbattery channel=5>";		
$txbattery6 = "<#txbattery channel=6>";		
$txbattery7 = "<#txbattery channel=7>";		
$txbattery8 = "<#txbattery channel=8>";
$StormRain = "<#StormRain>";
$StormRainStart = "<#StormRainStart>";

//-- Section FINE OFFSET --
$Light = "<#Light>";
$SensorContactLost = "<#SensorContactLost>";

//-- Section WEBTAGS SYSTEM --
$OsVersion = "<#OsVersion>";
$OsLanguage = "<#OsLanguage>";
$SystemUpTime = "<#SystemUpTime>";
$ProgramUpTime = "<#ProgramUpTime>";
$CpuName = "<#CpuName>";
$CpuCount = "<#CpuCount>";
$MemoryStatus = "<#MemoryStatus>";
$DisplayMode = "<#DisplayMode>";
$AllocatedMemory = "<#AllocatedMemory>";
$DiskSize = "<#DiskSize>";
$DiskFree = "<#DiskFree>";

//-- Section WEBTAGS without COMMAS --
$RCdew = "<#RCdew>";
$RCheatindex = "<#RCheatindex>";
$RChum = "<#RChum>";
$RCinhum = "<#RCinhum>";
$RCintemp = "<#RCintemp>";
$RCpress = "<#RCpress>";
$RCpressTH = "<#RCpressTH>";
$RCpressTL = "<#RCpressTL>";
$RCrfall = "<#RCrfall>";
$RCrrate = "<#RCrrate>";
$RCrrateTM = "<#RCrrateTM>";
$RCtemp = "<#RCtemp>";
$RCtempTH = "<#RCtempTH>";
$RCtempTL = "<#RCtempTL>";
$RCwchill = "<#RCwchill>";
$RCwgust = "<#RCwgust>";
$RCwgustTM = "<#RCwgustTM>";
$RCwspeed = "<#RCwspeed>";
$RCwlatest = "<#RCwlatest>"; 
$RCdewpointTH = "<#RCdewpointTH>"; 
$RCdewpointTL = "<#RCdewpointTL>";
$RCwchillTL = "<#RCwchillTL>"; 
$RCheatindexTH = "<#RCheatindexTH>";
$RCapptempTH = "<#RCapptempTH>"; 
$RCapptempTL = "<#RCapptempTL>";
$RCRecentOutsideTemp = "<#RCRecentOutsideTemp>";
$RCRecentWindSpeed = "<#RCRecentWindSpeed>";
$RCRecentWindGust = "<#RCRecentWindGust>";
$RCRecentWindLatest = "<#RCRecentWindLatest>";
$RCRecentWindChill = "<#RCRecentWindChill>";
$RCRecentDewPoint = "<#RCRecentDewPoint>";
$RCRecentHeatIndex = "<#RCRecentHeatIndex>";
$RCRecentPressure = "<#RCRecentPressure>";
$RCRecentRainToday = "<#RCRecentRainToday>";
$RCRecentRainToday = "<#RCRecentRainToday>";
$RCRecentUV = "<#RCRecentUV>";
?>
