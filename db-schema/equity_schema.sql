
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

create table if not exists trendlyne(
 comp_name text,
 comp_isin text,
 comp_bat text,
 comp_bar text,
 comp_der text,
 comp_roce3 text,
 comp_dpr2 text,
 comp_pledge text
);

create table screener(
rank text,
name text,
bse_code text,
nse_code text,
industry text,
captype text,
reco_type text,
reco_cause text,
cmp text,
mcap text,
sales text,
np text,
d2e text,
roe3 text,
roce3 text,
dp3 text,
dp text,
dy text,
pe text,
pe5 text,
peg text,
p2bv text,
p2sales text,
ev2ebitda text,
ev text,
opm text,
cr text,
sales5 text,
profit5 text,
pledge text,
piotski text);