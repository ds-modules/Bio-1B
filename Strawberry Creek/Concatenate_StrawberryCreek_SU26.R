library(dplyr)
library(googlesheets4)
library(googledrive)

## Email address with access to spreadsheets
gs4_auth(email = "david9456@berkeley.edu")
drive_auth(email = "david9456@berkeley.edu")

## Read spreadsheets
sec101_url <- "https://docs.google.com/spreadsheets/d/1A-nug1mjv9iR7L4Qbk16sxmwgbPCbKVo1ikvZ5ZQKXI/edit?usp=sharing"
sec102_url <- "https://docs.google.com/spreadsheets/d/1OrTJh7VcfCuIw3W5Qz8a0hNBXF3VMGHcIvxCJ1caBlY/edit?usp=sharing"
sec103_url <- "https://docs.google.com/spreadsheets/d/1oarsuS0OecRZKX2d2WtHG44JJZOcazNkxdOGWF3VUsM/edit?usp=sharing"
sec105_url <- "https://docs.google.com/spreadsheets/d/1D_EYyCAEpC4yc6tFJWLUpiaPHy_rCJA9VwsMNXLpQgQ/edit?usp=sharing"

secs <- c(101, 102, 103, 105)

## Column names of environmental variables of interest
env_vars <- c(
  "Site",
  "Plant Biodiversity",
  "Canopy Cover",
  "EC",
  "pH",
  "Temp (C)",
  "Phosphate (ppm)",
  "Nitrate (ppm)",
  "Dissolved Oxygen (1mg/L)",
  "Coliform Bacteria CFUs/100mL",
  "E.coli bacteria (CFUs/100mL)"
)

# Sections do not spell the canopy cover header identically, so every variant is
# renamed back to the name used in env_vars before the tables are combined.
canopy_aliases <- c(
  "Canopy Cover" = "Canopy Cover %",
  "Canopy Cover" = "Canopy Cover (%)",
  "Canopy Cover" = "Canopy Cover(%)"
)

# This function collapses observations for the same variable at the same site into
# a single entry by taking their mean; if there are multiple entries for
# the same variable at the same site but some of them are non-numeric, it
# excludes the non-numeric entries from the calculation. If no numeric entry
# exists for that site's variable, it gives NA for that entry.
mean_numeric_or_na <- function(x) {
  x <- trimws(as.character(x))
  x[x == ""] <- NA_character_
  x[x == "NA"] <- NA_character_

  # Some counts are typed with thousands separators, e.g. "10,400".
  x <- gsub(",", "", x, fixed = TRUE)

  nums <- suppressWarnings(as.numeric(x))
  nums <- nums[!is.na(nums)]

  if (length(nums) == 0) {
    NA_real_
  } else {
    mean(nums)
  }
}

# Fork and restoration status are recorded per row rather than in a separate site
# table, and the same site is occasionally labelled inconsistently, so the label
# used for a site is the one it carries most often.
most_common <- function(x) {
  x <- trimws(as.character(x))
  x <- x[!is.na(x) & x != "" & x != "NA"]

  if (length(x) == 0) {
    NA_character_
  } else {
    names(sort(table(x), decreasing = TRUE))[1]
  }
}

# Read each spreadsheet and collapse them into a single table...
# All spreadsheets are expected to have everything recorded in the sheet
# titled "Sheet1". Otherwise it will throw an error.
data_secs <- lapply(secs, function(s) {
  raw <- read_sheet(
    ss = get(paste0("sec", s, "_url")),
    sheet = "Sheet1",
    col_types = "c"
  ) |>
    mutate(across(everything(), as.character)) |>
    mutate(across(everything(), trimws)) |>
    rename(any_of(canopy_aliases))

  # Not every section sheet carries the restoration column.
  if (!"Restored vs Unrestored" %in% names(raw)) {
    raw$`Restored vs Unrestored` <- NA_character_
  }

  raw |>
    mutate(section_source = as.character(s), .before = 1)
})
names(data_secs) <- paste0("sec", secs)

all_raw <- bind_rows(data_secs) |>
  mutate(across(everything(), as.character)) |>
  mutate(across(everything(), trimws)) |>
  filter(!is.na(Site), Site != "", Site != "NA") |>
  select(any_of(c("section_source", "Fork", "Restored vs Unrestored", env_vars)))

site_tbl <- all_raw |>
  group_by(Site) |>
  summarise(
    Fork = most_common(Fork),
    Restoration = most_common(`Restored vs Unrestored`),
    .groups = "drop"
  ) |>
  mutate(
    Fork = recode(Fork, N = "North", S = "South"),
    Restoration = recode(Restoration, R = "Yes", U = "No")
  )

site_level <- all_raw |>
  group_by(Site) |>
  summarise(
    across(
      all_of(env_vars[-1]),
      mean_numeric_or_na
    ),
    .groups = "drop"
  )

# Write the final table
final_tbl <- site_tbl |>
  left_join(site_level, by = "Site") |>
  select(
    Site,
    Fork,
    Restoration,
    `Plant Biodiversity`,
    `Canopy Cover`,
    EC,
    pH,
    `Temp (C)`,
    `Phosphate (ppm)`,
    `Nitrate (ppm)`,
    `Dissolved Oxygen (1mg/L)`,
    `Coliform Bacteria CFUs/100mL`,
    `E.coli bacteria (CFUs/100mL)`
  )

# Save the final table to google drives
# When you re-run the script and overwrite the spreadsheet file, it will
# generate a new url for that sheet, so the link in the Jupyter
# Notebook should be manually fixed.
folder <- as_id("1MYpC3AyPB0dwFucEuUOUDXwIx_DpAKNX")

ss <- gs4_create(
  "Pooled Student Data",
  sheets = list(Sheet1 = final_tbl)
)

drive_mv(
  ss,
  path = folder,
  name = "Pooled Student Data",
  overwrite = TRUE
)
