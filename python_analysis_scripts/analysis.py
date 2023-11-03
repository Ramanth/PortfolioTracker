from super_portfolio import calculate_profit_loss_of_portfolio
from utils import show_net_pl_using_transactions, show_pl_with_current_price

# PL analysis for the purchases made on dates vs current price
# print("PL analysis for the purchases made on dates vs current price")
show_net_pl_using_transactions("2023-10-30 00:00:00", "2023-11-04 00:00:00")
print("\n")


def print_metrics(result_df):
    print(result_df)
    invested = int(result_df['Invested'].sum())
    print("Invested " + str(invested))
    print("NAV Value: " + str(int(result_df['AvgPrice'].sum())))

    filtered_df = result_df[result_df['Quantity'] > 0 ]
    print("Curr NAV Value: " + str(int(filtered_df['price'].sum())))
    print("Units : "+ str(int(invested/ result_df['AvgPrice'].sum())))
    print("Portfolio PL:  " + str(int(result_df['Profit_Loss'].sum())))
    print("20% growth profit :  " + str(int(result_df['If20% growth'].sum())))
    print("\n")

#super portfolio analysis
print("super portfolio analysis")
print("-----------------------")
result_df = calculate_profit_loss_of_portfolio("super_portfolio")
print_metrics(result_df)


# sub portfolio analysis
print("sub portfolio analysis")
print("-----------------------")
result_df = calculate_profit_loss_of_portfolio("sub_portfolio")
print_metrics(result_df)


# sub portfolio analysis
print("waya portfolio analysis")
print("-----------------------")
result_df = calculate_profit_loss_of_portfolio("waya_portfolio")
print_metrics(result_df)


# RISKY portfolio analysis
print("risky portfolio analysis")
print("-----------------------")
result_df = calculate_profit_loss_of_portfolio("risky_portfolio")
print_metrics(result_df)