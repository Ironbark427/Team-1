# Team 1 LendingClub primary notebook
# import dependencies
import pandas as pd
import numpy as np  # needed for replace nan code below
import glob

# PROCESSING OF LENDING CLUB LOAN FILES

# pull in all csvs and merge them into a single dataframe
bigdf = pd.concat([pd.read_csv(f, low_memory=False) for f in
                   glob.glob('data/LoanStats*.csv')], ignore_index=True)

# drop irrelevant rows
data = bigdf.drop([
    "id", "member_id", "url", "desc", "hardship_type", "hardship_reason",
    "hardship_status", "deferral_term", "hardship_amount",
    "hardship_start_date", "hardship_end_date", "payment_plan_start_date",
    "hardship_length", "hardship_dpd", "hardship_loan_status",
    "orig_projected_additional_accrued_interest",
    "hardship_payoff_balance_amount", "hardship_last_payment_amount",
    "debt_settlement_flag_date", "settlement_status", "settlement_date",
    "loan_amnt", "funded_amnt", "grade", "sub_grade",
    "emp_title", "verification_status", "dti", "earliest_cr_line",
    "inq_last_6mths", "zip_code", "pub_rec", "revol_bal",
    "total_acc", "initial_list_status", "out_prncp", "out_prncp_inv",
    "total_pymnt", "total_pymnt_inv", "total_rec_prncp", "total_rec_int",
    "last_pymnt_d", "last_pymnt_amnt", "next_pymnt_d", "last_credit_pull_d",
    "collections_12_mths_ex_med", "policy_code", "application_type",
    "annual_inc_joint", "dti_joint", "verification_status_joint",
    "acc_now_delinq", "tot_coll_amt", "tot_cur_bal", "open_acc_6m",
    "open_act_il", "open_il_12m", "open_il_24m", "mths_since_rcnt_il",
    "total_bal_il", "il_util", "open_rv_12m", "open_rv_24m", "max_bal_bc",
    "all_util", "total_rev_hi_lim", "inq_fi", "total_cu_tl", "inq_last_12m",
    "acc_open_past_24mths", "avg_cur_bal", "bc_open_to_buy", "bc_util",
    "num_accts_ever_120_pd", "num_actv_bc_tl", "num_actv_rev_tl",
    "num_bc_sats", "num_bc_tl", "num_il_tl", "num_op_rev_tl",
    "num_rev_accts", "num_rev_tl_bal_gt_0", "num_sats",
    "num_tl_120dpd_2m", "num_tl_30dpd", "num_tl_90g_dpd_24m",
    "num_tl_op_past_12m", "percent_bc_gt_75", "pub_rec_bankruptcies",
    "tax_liens", "tot_hi_cred_lim", "total_bal_ex_mort", "total_bc_limit",
    "total_il_high_credit_limit", "revol_bal_joint",
    "sec_app_earliest_cr_line", "sec_app_inq_last_6mths", "sec_app_mort_acc",
    "sec_app_open_acc", "sec_app_revol_util", "sec_app_num_rev_accts",
    "sec_app_chargeoff_within_12_mths", "sec_app_collections_12_mths_ex_med",
    "sec_app_mths_since_last_major_derog", "hardship_flag",
    "disbursement_method", "debt_settlement_flag",
    "debt_settlement_flag_date", "settlement_status", "settlement_date",
    "settlement_amount", "settlement_percentage", "settlement_term"], axis=1)

# code to fill nans with 0s
data['mths_since_last_major_derog'].replace(np.nan, 0)

# processing date into new columns
data["month_num"] = ""
data.loc[data['issue_d'].str[:3] == "Dec", ('month_num')] = (12)
data.loc[data['issue_d'].str[:3] == "Nov", ('month_num')] = (11)
data.loc[data['issue_d'].str[:3] == "Oct", ('month_num')] = (10)
data.loc[data['issue_d'].str[:3] == "Sep", ('month_num')] = (9)
data.loc[data['issue_d'].str[:3] == "Aug", ('month_num')] = (8)
data.loc[data['issue_d'].str[:3] == "Jul", ('month_num')] = (7)
data.loc[data['issue_d'].str[:3] == "Jun", ('month_num')] = (6)
data.loc[data['issue_d'].str[:3] == "May", ('month_num')] = (5)
data.loc[data['issue_d'].str[:3] == "Apr", ('month_num')] = (4)
data.loc[data['issue_d'].str[:3] == "Mar", ('month_num')] = (3)
data.loc[data['issue_d'].str[:3] == "Feb", ('month_num')] = (2)
data.loc[data['issue_d'].str[:3] == "Jan", ('month_num')] = (1)
data.loc[data['issue_d'].str[:3] == "", ('month_num')] = (0)

# clean up the dead rows
data.dropna(subset=['term', 'issue_d'], inplace=True)

# PROCESSING OF FEMA DISASTER FILE

# read in FEMA csv file into dataframe
fema = pd.read_csv('data/DisasterDeclarationsSummaries.csv')

# drop columns that are irrelevant
fema = fema.loc[:, ['disasterNumber', 'state', 'incidentBeginDate',
                    'incidentType', 'incidentEndDate']]

# create columns to link with lendingclub.com data
fema['yearBegin'] = fema['incidentBeginDate'].str[:4]
fema['monthBegin'] = fema['incidentBeginDate'].str[5:7]
fema['monthEnd'] = fema['incidentEndDate'].str[5:7]

# drop unix dates from dataframe
fema = fema.loc[:, ['disasterNumber', 'state', 'incidentType', 'yearBegin',
                    'monthBegin', 'monthEnd']]

# drop all data outside of 2018
fema = fema[fema['yearBegin'] == '2018']

# drop duplicate rows with same incident named for multiple counties
fema = fema.drop_duplicates(subset=['disasterNumber'], keep=False)

# fill in all ending month with beginning month if it is missing
fema.monthEnd.fillna(fema.monthBegin, inplace=True)

# drop irrelevant disasterNumber
fema.drop(columns=['disasterNumber'], inplace=True)

# convert month number strings to numeric
fema['monthBegin'] = fema['monthBegin'].apply(pd.to_numeric, errors='coerce')
fema['monthEnd'] = fema['monthEnd'].apply(pd.to_numeric, errors='coerce')
fema['aftermath'] = fema['monthEnd'] + 1

# reinforce the numeric status of loan month number
data['month_num'] = data['month_num'].apply(pd.to_numeric, errors='coerce')

# clean up the dead rows
fema.dropna(subset=['monthBegin', 'monthEnd'], inplace=True)
# write to csv
# fema.to_csv('data/fema_clean.csv', index=False)

# CREATING TRIGGER MARKS IN LENDING CLUB BASED ON FEMA

data["Disaster"] = ""
data["DState"] = ""
data["Aftermath"] = ""


# Returns "D" if there is an active disaster, "N" is no active disaster
def checkDisaster(row):
    global fema
    tmp_df = fema[(row['month_num'] >= fema['monthBegin'])
                  & (row['month_num'] <= fema['monthEnd'])
                  & (fema['state'] == row['addr_state'])]
    if len(tmp_df) > 0:
        return 'D'
    else:
        return 'N'


# Returns "A" if it is the month after a disaster, "N" is not aftermath
def checkAftermath(row):
    global fema
    tmp_df = fema[(row['month_num'] == fema['monthEnd']+1)
                  & (fema['state'] == row['addr_state'])]
    if len(tmp_df) > 0:
        return 'A'
    else:
        return 'N'


# Returns "T" if state has had a disaster that year, "F" if no disaster
def checkDState(row):
    global fema
    tmp_df = fema[(fema['state'] == row['addr_state'])]
    if len(tmp_df) > 0:
        return 'T'
    else:
        return 'F'


data['Disaster'] = data.apply(lambda x: checkDisaster(x), axis=1)
data['DState'] = data.apply(lambda x: checkDState(x), axis=1)
data['Aftermath'] = data.apply(lambda x: checkAftermath(x), axis=1)

data.to_csv('data/data_fema_compare.csv', index=False)
