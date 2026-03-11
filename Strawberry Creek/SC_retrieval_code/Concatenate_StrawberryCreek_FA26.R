library(dplyr)
library(googlesheets4)

## Email address with access to spreadsheets
gs4_auth(email = "david9456@berkeley.edu")

## Read spreadsheets
site_info <- "https://docs.google.com/spreadsheets/d/16-xACo886fx1QiEQZ0ok7hM3m3uU3ns3plLWhOnwksk/edit?usp=sharing"
sec111_url <- "https://docs.google.com/spreadsheets/d/1V77G8z2axpvAJfobTvfKqyP5-bhDd2OXZ7M_s9phPMQ/edit?usp=sharing"
sec112_url <- "https://docs.google.com/spreadsheets/d/19aqZ9Su-MVKt2A8QoeLG7Kzp9Mz7IGq3DkqIZdXPEgc/edit?usp=sharing"
sec113_url <- "https://docs.google.com/spreadsheets/d/113BOFt2imxXyWo2kHEVbsCU3id6bSRv5thx7UOImsjM/edit?usp=sharing"
sec121_url <- "https://docs.google.com/spreadsheets/d/1z544Y7EW2F9pjaFgl5LDSZRgDsJKG5TYeeuEMfhskL0/edit?usp=sharing"
sec122_url <- "https://docs.google.com/spreadsheets/d/1LJuC8awkgdIZu-Q-RJSYcSD-O2gIY-qUdpQ5WzA8-c0/edit?usp=sharing"
sec123_url <- "https://docs.google.com/spreadsheets/d/12bMmliGBFkQAhY2hM_xfPYQACaz3UWMUNlPUJmyHPOc/edit?usp=sharing"
sec211_url <- "https://docs.google.com/spreadsheets/d/1FJ8tti1aY3AqFdb4oNFONR4LbILn4-metPwB96kEq7k/edit?usp=sharing"
sec212_url <- "https://docs.google.com/spreadsheets/d/1190vk_FqVhwE4bKvHA9Pd9B-GLfYdlDjeol41V711rE/edit?usp=sharing"
sec213_url <- "https://docs.google.com/spreadsheets/d/11MhooECECdvB1mlggmszOlYrF62Ha5kM3ruWHv3Tgck/edit?usp=sharing"
sec221_url <- "https://docs.google.com/spreadsheets/d/1GtfK2LWSokBFVc6TL1r4id8bKf02yqF5RyUnYhtdWq0/edit?usp=sharing"
sec222_url <- "https://docs.google.com/spreadsheets/d/1lvWGjNkDKuUzdGTgSjn5s_GXEPqm1zSUq-bXR_pjHR8/edit?usp=sharing"
sec223_url <- "https://docs.google.com/spreadsheets/d/1BQ9k9L0bnRxLUj7a563kBycTqzPsDjaGtBQXCJJM9OE/edit?usp=sharing"
sec311_url <- "https://docs.google.com/spreadsheets/d/1Canh8PmENTztClMbsxi7D-BnZTMX4WLiWGElJZXt59Y/edit?usp=sharing"
sec312_url <- "https://docs.google.com/spreadsheets/d/13nFhNuHDj-sQ35szorbcY7Ts-dp7Bsqx1sV3r87NFio/edit?usp=sharing"
sec313_url <- "https://docs.google.com/spreadsheets/d/1-rQaHvb2bAe9Wus2sAN8SGK8HuVi3y209FtkcevmX8g/edit?usp=sharing"
sec321_url <- "https://docs.google.com/spreadsheets/d/11MiLBo8WIC-dCJPIPTygJlBU5BxYDzNkKX5frr55WCY/edit?usp=sharing"
sec322_url <- "https://docs.google.com/spreadsheets/d/14yQ57vCOmItAepNZ1mXwWU5paedcF93tl0o8bbY7q-g/edit?usp=sharing"
sec323_url <- "https://docs.google.com/spreadsheets/d/1nut1M_OnMLVMycpO5DDnmWtYI1r942Huf8neO5RU6tI/edit?usp=sharing"
sec411_url <- "https://docs.google.com/spreadsheets/d/1NIKWwGcWa8MrOZMvV_aimnL2YyBDgUD9BOFq2svLfY4/edit?usp=sharing"
sec412_url <- "https://docs.google.com/spreadsheets/d/1IEhLAIlTrXIlSMGAyVaGT53BDVOEw6jj7zHaVg5VZcc/edit?usp=sharing"
sec413_url <- "https://docs.google.com/spreadsheets/d/1h_4E-zNk3jRQwwF5OQrWOVAQzhbHu9JIWSEzWTzbJME/edit?usp=sharing"
sec421_url <- "https://docs.google.com/spreadsheets/d/1A-_pyRnBYmPP31dawcd4wLLzxtfWUtcbZWMyoLotMxs/edit?usp=sharing"
sec422_url <- "https://docs.google.com/spreadsheets/d/1UeE9eCM1ZkmGHxbrU8HYEaUIrzHLbSJw4v_c0ECZ-rc/edit?usp=sharing"
sec423_url <- "https://docs.google.com/spreadsheets/d/1YqE6H1R1msActN4sPp9yreU3Esz1vO-UU-JY76PtxhU/edit?usp=sharing"
sec512_url <- "https://docs.google.com/spreadsheets/d/1fP5OT1o3b2Nb28HQxhTdycvgdwt2B9J2YDM66rhlTLE/edit?usp=sharing"
sec513_url <- "https://docs.google.com/spreadsheets/d/1W8Gsw4Hb8-3xQsKGJ5CgnjqhQInxeX0j_o1kmPGfw_I/edit?usp=sharing"

secs <- c(
  111, 112, 113, 121, 122, 123, 211, 212, 213, 221, 222, 223,
  311, 312, 313, 321, 322, 323, 411, 412, 413, 421, 422, 423, 512, 513
)

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
  "E.coli bacteria (CFUs/100mL)",
  "Metric 1: Total Vegetation Cover",
  "Metric 2: Vegetation Structure",
  "Metric 3: Vegetation Quality",
  "Metric 4: Age Diversity",
  "Metric 5: Riparian Vegetation Width",
  "Metric 6: Riparian Soil Condition",
  "Metric 7: Macroinvertebrate Habitat Patch Richness",
  "Metric 8: Anthropogenic Altertations"
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
  
  nums <- suppressWarnings(as.numeric(x))
  nums <- nums[!is.na(nums)]
  
  if (length(nums) == 0) {
    NA_real_
  } else {
    mean(nums)
  }
}

# Read each spreadsheet and collapse them into a single table...
# All spreadsheets are expected to have everything recorded in the sheet
# titled "Sheet1". Otherwise it will throw an error.
data_secs <- lapply(secs, function(s) {
  read_sheet(
    ss = get(paste0("sec", s, "_url")),
    sheet = "Sheet1",
    col_types = "c"
  ) |>
    mutate(across(everything(), as.character)) |>
    mutate(across(everything(), trimws)) |>
    mutate(section_source = as.character(s), .before = 1)
})
names(data_secs) <- paste0("sec", secs)

site_tbl <- read_sheet(
  ss = site_info,
  col_types = "c"
) |>
  mutate(across(everything(), as.character)) |>
  mutate(across(everything(), trimws)) |>
  rename(Site_Fork = Fork) |>
  select(Site, Site_Fork, `Major restoration since 2000?`)

all_raw <- bind_rows(data_secs) |>
  mutate(across(everything(), as.character)) |>
  mutate(across(everything(), trimws)) |>
  filter(!is.na(Site), Site != "", Site != "NA") |>
  select(any_of(c("section_source", env_vars)))

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
  rename(
    Fork = Site_Fork,
    Restoration = `Major restoration since 2000?`
  ) |>
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
    `E.coli bacteria (CFUs/100mL)`,
    `Metric 1: Total Vegetation Cover`,
    `Metric 2: Vegetation Structure`,
    `Metric 3: Vegetation Quality`,
    `Metric 4: Age Diversity`,
    `Metric 5: Riparian Vegetation Width`,
    `Metric 6: Riparian Soil Condition`,
    `Metric 7: Macroinvertebrate Habitat Patch Richness`,
    `Metric 8: Anthropogenic Altertations`
  )

final_tbl
