from stockx import Stockx
# Gets prices from each site


class Prices:

    def __init__(self, driver, sku, email, password, t, rate_gbp, price, date, last_month, current_month):
        self.driver = driver
        self.sku = sku
        self.email = email
        self.password = password
        self.t = t
        self.rate_gbp = rate_gbp
        self.price = price
        self.date = date
        self.last_month = last_month
        self.current_month = current_month

    def stockx(self):
        st = Stockx(self.driver, self.sku, self.email, self.password, self.price, self.rate_gbp, self.date,
                    self.last_month, self.current_month)
        if self.t == 0:
            st.region()
            st.logging_in()
        try:
            list_stockx = st.item_info()
            return [list_stockx[0], list_stockx[1]]
        except Exception:
            return ['Error', 'Error']
