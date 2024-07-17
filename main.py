# Bellevue 2023
interest_rate = 0.07
property_tax = 0.0071
maintainence_and_renovation = 0.01
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

"""
# Initial Cost:
# Initial costs are the costs you incur when you go to the closing for the home
# you are purchasing. This includes the down payment and other fees.

# Reccuring Costs:
# "Recurring costs are expenses you will have to pay monthly or yearly in
# owning your home. These include mortgage payments; condo fees (or other
# community living fees); maintenance and renovation costs; property taxes; and
# homeowner’s insurance. A few items are tax deductible, up to a point: property
# taxes; the interest part of the mortgage payment; and, in some cases, a
# portion of the common charges.
# The resulting tax savings are accounted for in the buying total. If your
# house-related deductions are similar to or smaller than the standard deduction,
# you’ll get little or no relative tax savings from buying. If your house-related
# deductions are large enough to make itemizing worthwhile, we only count as
# savings the amount above the standard deduction.

# Opportunity Costs:
# Opportunity costs are calculated for the initial purchase costs and for the
# recurring costs. That will give you an idea of how much you could have made if
# you had invested your money instead of buying your home.

# Net Proceeds:
# Net proceeeds is the amount of money you receive from the sale of your home
# minus the closing costs, which includes the broker’s commission and other
# fees, the remaining principal balance that you pay to your mortgage bank and
# any tax you have to pay on profit that exceeds your capital gains exclusion.
# If your total is negative, it means you have done very well: You made enough
# of a profit that it covered not only the cost of your home, but also all of
# your recurring expenses.
"""

class Home:
    def __init__(self):
        self.price = 2000000
        self.down_payment = 0.2
        self.loan_years = 20
        self.plan_to_stay = 20

        # mandate this for now
        assert self.loan_years == self.plan_to_stay

        self.yearly_mortgage = self.yearly_mortgage()

    def initial_cost(self):
        return self.price * self.down_payment
    
    def recurring_cost_total(self):
        result = 0
        for year in range(1, self.plan_to_stay + 1):
            result = result + self.recurring_cost(year)
        return result

    def recurring_cost(self, year):
        value = self.home_value(year)
        return value * (property_tax + maintainence_and_renovation + home_insurance)

    def opportunity_cost(self):
        result = self.initial_cost() * pow(1 + investment_return, self.plan_to_stay)
        for year in range(0, self.plan_to_stay):
            cost = self.yearly_mortgage * (pow(1 + investment_return, self.plan_to_stay - year) - 1)
            result += cost
        return result

    def yearly_mortgage(self):
        # https://www.businessinsider.com/personal-finance/mortgage-calculator
        # M = P * (i (1 + i)^n) / ((1 + i)^n - 1)
        # P = principal, i = monthly interest rate, n = number of months
        p = self.price * (1 - self.down_payment)
        i = interest_rate / 12
        print(i)
        n = self.loan_years * 12
        monthly_mortgage = p * (i * pow(1 + i, n)) / (pow(1 + i, n) - 1)
        return monthly_mortgage * 12

    def net_proceeds(self):
        return self.selling_price() - self.closing_cost() - self.recurring_cost_total() - self.opportunity_cost()

    def selling_price(self):
        return self.home_value(self.plan_to_stay)

    def home_value(self, year):
        return self.price * pow(1 + home_growth, year)

    def closing_cost(self):
        selling = 0.06
        return selling * self.selling_price()

# 10%
rent_growth = 0.1

class Rent:
    def __init__(self):
        self.rent = 5000
        self.plan_to_stay = 20
    
    def net_proceeds(self):
        return 0 - self.recurring_cost_total() - self.opportunity_cost()

    def recurring_cost_total(self):
        result = 0
        for i in range(0, self.plan_to_stay):
            result += self.rent * 12 * pow(1 + rent_growth, i)
        return result

    def opportunity_cost(self):
        result = 0
        for year in range(0, self.plan_to_stay):
            cost = self.rent * 12 * (pow(1 + investment_return, self.plan_to_stay - year) - 1)
            result += cost
        return result

if __name__ == '__main__':
    home = Home()
    print("Buy: ", home.net_proceeds())
    rent = Rent()
    print("Rent:", rent.net_proceeds())
