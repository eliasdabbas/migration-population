import pandas as pd
from pandas_datareader import wb

wb_countries = wb.get_countries()
country_list = wb_countries[wb_countries['region']!='Aggregates']['name'].reset_index(drop=True)

indicator_ids = ['EN.POP.DNST', 'SP.POP.TOTL', 'SM.POP.NETM']

migration = wb.WorldBankReader(symbols=['SM.POP.NETM'], start=1950, end=2018, countries='all').read()
pop_density = wb.WorldBankReader(symbols=['EN.POP.DNST'], start=1950, end=2018, countries='all').read()
population = wb.WorldBankReader(symbols=['SP.POP.TOTL'], start=1950, end=2018, countries='all').read()

pop_density_countries = pop_density.reset_index()#.query('country in @country_list').reset_index(drop=True)
population_countries = population.reset_index()#.query('country in @country_list').reset_index(drop=True)
migration_countries = migration.reset_index()#.query('country in @country_list').reset_index(drop=True)

pop_density_merged = pd.merge(population_countries, pop_density_countries, on=['country', 'year'], how='outer')
migration_final = (pd.merge(pop_density_merged, migration_countries, on=['country', 'year'], how='outer')
                   .rename(columns={'SP.POP.TOTL': 'population',
                                    'EN.POP.DNST': 'pop_density',
                                    'SM.POP.NETM': 'net_migration'})
                   .assign(migration_perc=lambda df: df['net_migration'].div(df['population'])))

migration_final = pd.merge(migration_final, wb_countries, how='left', left_on='country', right_on='name')
migration_final.drop('name', axis=1).to_csv('migration_population.csv', index=False)