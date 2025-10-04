# Django E-commerce Shop with Stripe Integration

A simple Django-based e-commerce application with Stripe payment integration, featuring 3 fixed products and order management.

## 📋 Features

- **Product Display**: 3 fixed products with name, description, and price
- **Shopping Cart**: Select quantities for each product
- **Stripe Checkout**: Secure payment processing using Stripe Checkout
- **Order Management**: View all paid orders on the main page and dedicated orders page
- **Double-Charge Prevention**: Uses Stripe session IDs and order status to prevent duplicate charges
- **Webhook Support**: Stripe webhooks for reliable payment confirmation
- **Responsive Design**: Bootstrap 5 for mobile-friendly UI

## 🏗️ Architecture & Flow

### Payment Flow:
1. User selects product quantities on main page
2. Clicks "Buy Now" button
3. System creates a pending order in database
4. Redirects to Stripe Checkout (hosted by Stripe)
5. User completes payment
6. Stripe redirects back to success page
7. Order status updated to "paid"
8. Order appears in "My Orders" section

### Double-Charge Prevention:
- Each order has a unique Stripe session ID
- Order status checked before processing
- Webhooks provide server-side confirmation
- Idempotent operations (only process once)

## 🛠️ Tech Stack

- **Backend**: Django 4.2.7
- **Payment**: Stripe API
- **Database**: SQLite (default) / PostgreSQL (configurable)
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Environment**: Python 3.8+

## 📦 Installation & Setup

### Option 1: Docker (Recommended) 🐳

**Quick Start:**
```powershell
# Simple setup with SQLite
docker-compose -f docker-compose.simple.yml up --build

# Or full setup with PostgreSQL
docker-compose up --build
```

Visit: http://localhost:8000

**See [DOCKER.md](DOCKER.md) for complete Docker documentation.**

### Option 2: Manual Setup

### 1. Clone and Navigate
```bash
cd "c:\Users\deves\OneDrive\Desktop\tet\New folder (2)\stripe"
```

### 2. Create Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the project root:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe Test Keys (get from https://dashboard.stripe.com/test/apikeys)
STRIPE_PUBLIC_KEY=pk_test_51RgoHoIIZ6VYJk8v83G
STRIPE_SECRET_KEY=sk_test_51RgoHoIIZ6VcClX
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

SITE_URL=http://127.0.0.1:8000
```

### 5. Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Setup Products
```powershell
python manage.py setup_products
```

### 7. Create Admin User (Optional)
```powershell
python manage.py createsuperuser
```

### 8. Run Development Server
```powershell
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## 🔑 Stripe Configuration

### Get Test Keys:
1. Sign up at [Stripe](https://stripe.com)
2. Go to [API Keys](https://dashboard.stripe.com/test/apikeys)
3. Copy "Publishable key" → `STRIPE_PUBLIC_KEY`
4. Copy "Secret key" → `STRIPE_SECRET_KEY`

### Setup Webhooks (Optional but Recommended):
1. Install [Stripe CLI](https://stripe.com/docs/stripe-cli)
2. Login: `stripe login`
3. Forward webhooks to local:
   ```powershell
   stripe listen --forward-to localhost:8000/webhook/
   ```
4. Copy webhook secret → `STRIPE_WEBHOOK_SECRET`

### Test Cards:
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- Any future date for expiry, any 3 digits for CVC

## 📁 Project Structure

```
com/
├── shop/                      # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── payments/                  # Main app
│   ├── models.py             # Product, Order, OrderItem
│   ├── views.py              # Payment logic
│   ├── urls.py
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── setup_products.py
├── templates/
│   ├── base.html
│   └── payments/
│       ├── index.html        # Main page
│       ├── success.html      # Payment success
│       ├── cancel.html       # Payment cancelled
│       └── my_orders.html    # All orders
├── manage.py
├── requirements.txt
├── .env                      # Environment variables (create this)
└── README.md
```

## 💡 Key Implementation Details

### Double-Charge Prevention:
1. **Session ID Tracking**: Each checkout creates unique Stripe session
2. **Order Status**: Check `status == 'paid'` before processing
3. **Atomic Transactions**: Use `@transaction.atomic` for database operations
4. **Webhook Idempotency**: Only process events once
5. **Refresh Protection**: Success page checks existing order status

### Models:
- **Product**: Fixed products (3 items)
- **Order**: Tracks payment status and total
- **OrderItem**: Individual items in an order

### Views:
- `index`: Main page (products + orders)
- `create_checkout_session`: Creates Stripe session
- `success`: Handles successful payment
- `cancel`: Handles cancelled payment
- `stripe_webhook`: Processes Stripe events
- `my_orders`: Dedicated orders page

## 🧪 Testing

### Test the Flow:
1. Visit http://127.0.0.1:8000
2. Select quantities for products
3. Click "Buy Now"
4. Use test card: `4242 4242 4242 4242`
5. Complete payment
6. Verify order appears in "My Orders"
7. Refresh success page (should not create duplicate)

### Admin Panel:
- URL: http://127.0.0.1:8000/admin
- Manage products and view orders

## 🔒 Security Considerations

- ✅ CSRF protection enabled
- ✅ Stripe webhook signature verification
- ✅ Environment variables for secrets
- ✅ No credit card data stored locally
- ✅ Stripe handles PCI compliance
- ⚠️ Set `DEBUG=False` in production
- ⚠️ Use strong `SECRET_KEY` in production
- ⚠️ Use HTTPS in production

## 🚀 Deployment Considerations

### For Production:
1. Set `DEBUG=False`
2. Configure PostgreSQL database
3. Set up proper `ALLOWED_HOSTS`
4. Use environment variables
5. Configure webhook endpoint on Stripe Dashboard
6. Set up SSL certificate (HTTPS)
7. Use production Stripe keys
8. Run `python manage.py collectstatic`

## 📝 Assumptions & Design Decisions

1. **3 Fixed Products**: Hardcoded via management command
2. **No User Authentication**: Simplified for demo (can be added)
3. **Stripe Checkout**: Easier than Payment Intents for this use case
4. **SQLite Default**: Easy setup, switch to PostgreSQL for production
5. **No Shopping Cart Persistence**: Each purchase is independent
6. **Order History**: Shows all paid orders (can filter by user)

## ⏱️ Development Time

Estimated: 3-4 hours
- Project setup: 30 min
- Models & admin: 30 min
- Views & logic: 90 min
- Templates & styling: 60 min
- Testing & documentation: 30 min

## 🤖 AI Assistance

This project was built with assistance from GitHub Copilot for:
- Boilerplate code generation
- Django best practices
- Stripe integration patterns
- Documentation structure

## 📧 Support

For issues or questions:
1. Check Stripe Dashboard for payment logs
2. Check Django logs for errors
3. Verify environment variables are set
4. Test with Stripe CLI webhook forwarding

## 📜 License

This is a demonstration project for educational purposes.

## 🔗 Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Stripe Documentation](https://stripe.com/docs)
- [Stripe Checkout Guide](https://stripe.com/docs/payments/checkout)
- [Bootstrap Documentation](https://getbootstrap.com/)
