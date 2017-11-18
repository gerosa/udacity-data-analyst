
library(dplyr)

Sys.setlocale(category = "LC_ALL", locale = "pt_BR.UTF-8")
ds = read.csv("reclamacoes-fundamentadas-sindec-2015.csv", 
              sep=',', encoding='utf-8', stringsAsFactors = FALSE, strip.white = TRUE)

# keeping only columns used in this analysis
ds <- subset(ds, select=c(AnoCalendario, DataArquivamento, DataAbertura, UF,
                          Atendida))

# renaming columns
names(ds) <- c('year', 'closingDate', 'registerDate', 'state', 'resolved')

# replacing empty cells with NA
ds[ds == ''] <- NA
ds[ds == 'NULL'] <- NA

# removing rows with any missing value (NA)
ds <- na.omit(ds)

# fixing data types
ds$closingDate <- as.Date(ds$closingDate)
ds$registerDate <- as.Date(ds$registerDate)
ds$state <- as.factor(ds$state)
ds$resolved <- as.factor(ds$resolved)


ds$stateName <- recode(ds$state,
                       `AC` = 'Acre',
                       `AL` = 'Alagoas',
                       `AP` = 'Amapá',
                       `AM` = 'Amazonas',
                       `BA` = 'Bahia',
                       `CE` = 'Ceará',
                       `DF` = 'Distrito Federal',
                       `ES` = 'Espírito Santo',
                       `GO` = 'Goiás',
                       `MA` = 'Maranhão',
                       `MT` = 'Mato Grosso',
                       `MS` = 'Mato Grosso do Sul',
                       `MG` = 'Minas Gerais',
                       `PA` = 'Pará',
                       `PB` = 'Paraíba',
                       `PR` = 'Paraná',
                       `PE` = 'Pernambuco',
                       `PI` = 'Piauí',
                       `RJ` = 'Rio de Janeiro',
                       `RN` = 'Rio Grande do Norte',
                       `RS` = 'Rio Grande do Sul',
                       `RO` = 'Rondônia',
                       `RR` = 'Roraima',
                       `SC` = 'Santa Catarina',
                       `SP` = 'São Paulo',
                       `SE` = 'Sergipe',
                       `TO` = 'Tocantins')

# translating S (sim) to Y (yes)
ds$resolved <- recode(ds$resolved, S = 'Y', N = 'N')

# creating a new continuous variable
ds$elapsedDays <- as.numeric(ds$closingDate - ds$registerDate)

# calculate the frequency table for the state / resolved features
state_resolved <- ds %>%
  group_by(state, stateName, resolved) %>%
  summarise (n = n()) %>%
  mutate(freq = n / sum(n)) %>%
  subset(resolved == 'Y')

# calculate the median and mean elapsed days per state and resolved features
state_resolved_elapsedays <- ds %>%
  group_by(state, stateName, resolved) %>%
  summarise(median = median(elapsedDays), mean = mean(elapsedDays)) %>%
  subset(resolved == 'Y')

# joining the frequency table of states/resolved with the median elapsed days
state_resolvedrate_elapsedays <- state_resolved_elapsedays %>%
  left_join(state_resolved)

# rounding and exporting the data
state_resolvedrate_elapsedays$mean <- round(state_resolvedrate_elapsedays$mean) / 7
state_resolvedrate_elapsedays$median <- round(state_resolvedrate_elapsedays$median) / 7
state_resolvedrate_elapsedays$freq <- round(state_resolvedrate_elapsedays$freq, digits = 3)


write.table(state_resolvedrate_elapsedays, file = "data.tsv",
            quote = FALSE, sep = "\t", row.names=FALSE)
