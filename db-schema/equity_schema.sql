
create table if not exists amfi( 
sno text,
company_name text,
isin text,
bse_symbol text,
nse_symbol text,
avg_mcap text,
cap_type text
);

create table if not exists isin(
company_name text,
industry_name text,
symbol_ticker text,
series text,
isin_code text
);

create table if not exists demat_summary(
stock_symbol text,
company_name text,
isin_code text,
qty text,
acp text,
cmp text,
pct_change text,
value_cost text,
value_market text,
realized_pl text,
unrealized_pl text,
unrealized_pl_pct text,
unused1 text
);

create table if not exists demat_txn(
stock_symbol text,
company_name text,
isin_code text,
action text,
quantity text,
txn_price text,
brokerage text,
txn_charges text,
stamp_duty text,
segment text,
stt text,
remarks text,
txn_date text,
exchange text,
unused1 text
);

create table if not exists plan(
comp_industry text,
comp_name text,
comp_ticker text,
comp_selected text,
comp_desc text
);

create table if not exists weight(
 comp_ticker text,
 comp_weight_type text,
 comp_weight_units text
);