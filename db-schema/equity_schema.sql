
drop table amfi;
drop table isin;

create table if not exists amfi( 
sno text,
company_name text,
isin text,
bse_symbol text,
bse_mcap  text,
nse_symbol text,
nse_mcap  text,
mse_symbol text,
mse_mcap  text,
avg_mcap text,
cap_type text,
unused1 text,
unused2 text
);

create table if not exists isin(
company_name text,
industry_name text,
symbol_ticker text,
series text,
isin_code text
);
