# Example automated data pipeline for Luke F. Miller's portfolio
#
# TO REPLACE THE DATA SOURCE:
# 1. Change source_url.
# 2. Replace the parsing block that creates `clean`.
# 3. Keep the output column names aligned with docs/assets/dashboard.js,
#    or change the JavaScript to match your new columns.

source_url <- "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
output_dir <- file.path("docs", "data")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

if (!requireNamespace("jsonlite", quietly = TRUE)) {
  stop("Package 'jsonlite' is required. Install it with install.packages('jsonlite').")
}

message("Downloading USGS earthquake feed...")
payload <- jsonlite::fromJSON(source_url, simplifyVector = FALSE)

if (is.null(payload$features) || !is.list(payload$features)) {
  stop("The source did not contain the expected GeoJSON features array.")
}

`%||%` <- function(x, fallback) if (is.null(x) || length(x) == 0) fallback else x

rows <- lapply(payload$features, function(feature) {
  coordinates <- feature$geometry$coordinates
  properties <- feature$properties
  event_time <- as.POSIXct(as.numeric(properties$time %||% NA_real_) / 1000, origin = "1970-01-01", tz = "UTC")
  data.frame(
    event_id = as.character(feature$id %||% ""),
    time_utc = if (is.na(event_time)) "" else format(event_time, "%Y-%m-%dT%H:%M:%SZ"),
    magnitude = as.numeric(properties$mag %||% NA_real_),
    place = as.character(properties$place %||% "Location not reported"),
    longitude = as.numeric(coordinates[[1]] %||% NA_real_),
    latitude = as.numeric(coordinates[[2]] %||% NA_real_),
    depth_km = as.numeric(coordinates[[3]] %||% NA_real_),
    detail_url = as.character(properties$url %||% ""),
    stringsAsFactors = FALSE
  )
})

clean <- do.call(rbind, rows)
clean <- clean[!is.na(clean$magnitude) & !is.na(clean$latitude) & !is.na(clean$longitude), ]
clean <- clean[order(clean$time_utc, decreasing = TRUE), ]

if (nrow(clean) == 0) stop("Validation failed: no usable earthquake records were found.")
if (any(clean$magnitude < -10 | clean$magnitude > 10)) stop("Validation failed: magnitude outside expected range.")
if (any(clean$latitude < -90 | clean$latitude > 90)) stop("Validation failed: latitude outside expected range.")

write.csv(clean, file.path(output_dir, "earthquakes.csv"), row.names = FALSE, na = "")

metadata <- list(
  generated_at_utc = format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
  source_name = "U.S. Geological Survey - All Earthquakes, Past Day",
  source_url = source_url,
  record_count = nrow(clean)
)
jsonlite::write_json(metadata, file.path(output_dir, "metadata.json"), auto_unbox = TRUE, pretty = TRUE)
message(sprintf("Wrote %s validated records.", nrow(clean)))
