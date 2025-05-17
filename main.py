import math

# Bellevue 2023
interest_rate = 0.07
property_tax = 0.0071
maintainence_and_renovation = 0.01
# national average-ish
home_insurance = 0.0055

# Data point 1 -- https://www.zillow.com/home-values/3619/bellevue-wa/
# Bellevue
# 678k in 2016-03, 1,396k in 2024-03
# 9.4% = Math.pow(1396 / 678, 1. / 8)
# Data point 2 -- https://fred.stlouisfed.org/series/ATNHPIUS42644Q
# Seattle-Bellevue-Kent
# 1995 Q1 index 100, 2024 Q1 index 521.5
# 5.7% = Math.pow(5.02, 1. / 29)
home_growth = 0.094 # Use data point 1

# Last page of https://www.berkshirehathaway.com/letters/2023ltr.pdf
# 1962 - 2023 Not adjusted for inflation
investment_return = 0.102

def my_print(text, num):
    print(f"{text:<20}:  {num}")

def print_bar():
    for i in range(0, 45):
        print('-', end='')
    print("")

class Home:
    def __init__(self):
        self.price = 2000000 # 2M
        self.down_payment = math.ceil(self.price * .2)
        self.total_loan = self.price - self.down_payment
        self.loan_years = 20
        self.plan_to_stay = 20
        # mandate this for now
        assert self.loan_years == self.plan_to_stay
        self.yearly_mortgage = math.ceil(self.yearly_mortgage())
        my_print("Total Price", self.price)
        my_print("Down Payment", self.down_payment)
        my_print("Total Loan", self.total_loan)
        my_print("Loan Years", self.loan_years)
        my_print("Yearly mortgage", self.yearly_mortgage)

    def initial_cost(self):
        return self.down_payment
    
    def recurring_cost_total(self):
        result = 0
        for year in range(1, self.plan_to_stay + 1):
            result = result + self.recurring_cost(year)
        return int(result)

    def recurring_cost(self, year):
        value = self.home_value(year)
        return value * (property_tax + maintainence_and_renovation + home_insurance)

    def opportunity_cost(self):
        result = self.initial_cost() * (pow(1 + investment_return, self.plan_to_stay) - 1)
        rent = Rent()
        for year in range(0, self.plan_to_stay):
            yearly = self.yearly_mortgage + self.recurring_cost(year)
            yearly_delta = yearly - 12 * rent.rent
            cost = yearly_delta * (pow(1 + investment_return, year) - 1)
            result += cost
        return int(result)

    def yearly_mortgage(self):
        # https://www.businessinsider.com/personal-finance/mortgage-calculator
        # M = P * (i (1 + i)^n) / ((1 + i)^n - 1)
        # P = principal, i = monthly interest rate, n = number of months
        p = self.price - self.down_payment
        i = interest_rate / 12
        n = self.loan_years * 12
        monthly_mortgage = p * (i * pow(1 + i, n)) / (pow(1 + i, n) - 1)
        return monthly_mortgage * 12

    def net_proceeds(self):
        selling_price = self.selling_price()
        closing_cost = self.closing_cost()
        recurring_cost_total = self.recurring_cost_total()
        opportunity_cost = self.opportunity_cost()
        print_bar()
        my_print("Selling Price", selling_price)
        my_print("Closing Cost", closing_cost)
        my_print("Recurring Cost Total", recurring_cost_total)
        my_print("Opportunity Cost", opportunity_cost)
        result = self.selling_price() - self.closing_cost() - self.recurring_cost_total() - self.opportunity_cost()
        return int(result)

    def selling_price(self):
        result = self.home_value(self.plan_to_stay)
        return int(result)

    def home_value(self, year):
        return self.price * pow(1 + home_growth, year)

    def closing_cost(self):
        selling = 0.06
        result = selling * self.selling_price()
        return int(result)

# 10%
rent_growth = 0.1

class Rent:
    def __init__(self):
        self.rent = 4000
        self.plan_to_stay = 20
    
    def net_proceeds(self):
        # Do not consider opportunity cost because we deducted this while calculating
        # buying Home's opportunity cost.
        result = -self.recurring_cost_total() #- self.opportunity_cost()
        return int(result)

    def recurring_cost_total(self):
        result = 0
        for i in range(0, self.plan_to_stay):
            result += self.rent * 12 * pow(1 + rent_growth, i)
        return result

    # def opportunity_cost(self):
    #     result = 0
    #     for year in range(0, self.plan_to_stay):
    #         cost = self.rent * 12 * (pow(1 + investment_return, self.plan_to_stay - year) - 1)
    #         result += cost
    #     return result

if __name__ == '__main__':
    home = Home()
    # print("----------------------------------------------------")
    home_net_proceeds = home.net_proceeds()
    print_bar()
    my_print("Buy", home_net_proceeds)
    rent = Rent()
    my_print("Rent", rent.net_proceeds())
