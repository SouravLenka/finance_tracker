def categorize_transaction(description: str) -> str:
    """
    Categorizes a transaction description into a meaningful category
    based on real merchant patterns found in the bank statement.
    """

    if not description:
        return "Other"

    d = description.lower()

    # ---------------- FOOD & GROCERY ----------------
    if any(k in d for k in [
        "soda", "galaxy", "mirchi", "biryani", "fast food", "tiffin",
        "canteen", "bakery", "sweet", "mithan", "ice cream", "juice",
        "hotel", "restaurant", "dahibara", "tea", "chai",
        "food villa", "purnima", "ganesh tiffins",
        "maa majhigouri", "sahoo sweet", "chaska", "dolly",
        "narayan", "bapun"
    ]):
        return "Food & Grocery"

    # ---------------- ONLINE SHOPPING ----------------
    if any(k in d for k in [
        "amazon", "flipkart", "myntra", "ajio", "meesho"
    ]):
        return "Online Shopping"

    # ---------------- OFFLINE SHOPPING ----------------
    if any(k in d for k in [
        "zudio", "vishal mega mart", "reliance smart",
        "mk mart", "ms jain", "darshan textiles",
        "friends watch"
    ]):
        return "Shopping"

    # ---------------- TRANSPORT & TRAVEL ----------------
    if any(k in d for k in [
        "ixigo", "irctc", "redbus", "ola", "uber",
        "rapido", "ticket", "metro", "bus",
        "service station", "bike point", "petrol"
    ]):
        return "Transport"

    # ---------------- BILLS & SUBSCRIPTIONS ----------------
    if any(k in d for k in [
        "recharge", "jio", "airtel", "vi",
        "electricity", "bill", "google play"
    ]):
        return "Bills & Subscriptions"

    # ---------------- EDUCATION ----------------
    if any(k in d for k in [
        "giet", "college", "campus"
    ]):
        return "Education"

    # ---------------- ACCOMMODATION ----------------
    if any(k in d for k in [
        "room", "rent", "nc8", "divyajyoti",
        "anshuman", "chiranjeebi"
    ]):
        return "Accommodation"

    # ---------------- ENTERTAINMENT ----------------
    if any(k in d for k in [
        "spotify", "netflix", "prime", "hotstar", "audio"
    ]):
        return "Entertainment"

    # ---------------- HEALTH ----------------
    if any(k in d for k in [
        "hospital", "clinic", "medical", "pharmacy"
    ]):
        return "Healthcare"

    # ---------------- INCOME ----------------
    if any(k in d for k in [
        "received from", "credited", "salary", "papa"
    ]):
        return "Income"

    # ---------------- PERSONAL TRANSFERS ----------------
    if any(k in d for k in [
        "paid to", "upi", "transfer"
    ]):
        return "Personal Transfers"

    return "Other"
