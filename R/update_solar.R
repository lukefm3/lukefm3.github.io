# Hawai'i Solar Research Monitor
# Downloads current hourly weather-model data for four island locations and
# converts shortwave radiation into an illustrative PV output estimate.

if (!requireNamespace("jsonlite", quietly = TRUE)) stop("Package 'jsonlite' is required.")
output_dir <- file.path("docs", "data")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
locations <- data.frame(location=c("Honolulu","Kahului","Hilo","Lihue"),island=c("Oahu","Maui","Hawaii Island","Kauai"),latitude=c(21.3069,20.8893,19.7074,21.9747),longitude=c(-157.8583,-156.4729,-155.0885,-159.3681),stringsAsFactors=FALSE)
performance_ratio <- 0.80
fetch_location <- function(place,island,latitude,longitude){
  endpoint <- paste0("https://api.open-meteo.com/v1/forecast?latitude=",latitude,"&longitude=",longitude,"&hourly=temperature_2m,cloud_cover,shortwave_radiation&timezone=Pacific%2FHonolulu&past_days=2&forecast_days=7")
  message("Downloading solar forecast for ",place,"...")
  payload <- jsonlite::fromJSON(endpoint); hourly <- payload$hourly
  required <- c("time","temperature_2m","cloud_cover","shortwave_radiation")
  if(is.null(hourly)||!all(required%in%names(hourly))) stop("Unexpected API response for ",place)
  radiation <- pmax(as.numeric(hourly$shortwave_radiation),0)
  data.frame(location=place,island=island,latitude=latitude,longitude=longitude,time_local=as.character(hourly$time),date_local=substr(as.character(hourly$time),1,10),temperature_c=as.numeric(hourly$temperature_2m),cloud_cover_pct=as.numeric(hourly$cloud_cover),shortwave_wm2=radiation,modeled_kw_per_kw=radiation/1000*performance_ratio,modeled_kwh_per_kw=radiation/1000*performance_ratio,stringsAsFactors=FALSE)
}
rows <- Map(fetch_location,locations$location,locations$island,locations$latitude,locations$longitude)
clean <- do.call(rbind,rows)
if(nrow(clean)<500) stop("Validation failed: too few hourly records.")
if(any(!is.finite(clean$shortwave_wm2))||any(clean$shortwave_wm2<0)) stop("Validation failed: invalid solar-radiation values.")
if(any(clean$cloud_cover_pct<0|clean$cloud_cover_pct>100,na.rm=TRUE)) stop("Validation failed: cloud cover outside 0-100%.")
write.csv(clean,file.path(output_dir,"hawaii_solar.csv"),row.names=FALSE,na="")
metadata <- list(generated_at_utc=format(Sys.time(),"%Y-%m-%dT%H:%M:%SZ",tz="UTC"),source_name="Open-Meteo Weather Forecast API",source_url="https://open-meteo.com/en/docs",locations=nrow(locations),record_count=nrow(clean),performance_ratio=performance_ratio,model_description="Illustrative hourly output for a 1 kW PV system: shortwave radiation / 1000 x 0.80. Not measured generation or a site-specific engineering estimate.")
jsonlite::write_json(metadata,file.path(output_dir,"solar_metadata.json"),auto_unbox=TRUE,pretty=TRUE)
message(sprintf("Wrote %s validated hourly solar records.",nrow(clean)))
