# Stripe Payment Integration - Future Implementation Notes

This document outlines how to integrate Stripe payment subscription into the signup flow.

## 🎯 Goal

When users sign up, they should:
1. Fill out signup form
2. Be redirected to Stripe payment page
3. Pay monthly subscription fee
4. After successful payment, account is created
5. User is automatically logged in

## 📋 Implementation Steps

### Step 1: Install Stripe Dependencies

**Frontend:**
```bash
npm install @stripe/stripe-js @stripe/react-stripe-js
```

**Backend:**
```bash
pip install stripe
```

### Step 2: Backend Changes Needed

1. **Create Stripe Customer Endpoint**
   ```python
   POST /api/stripe/create-customer
   # Creates Stripe customer and returns customer_id
   ```

2. **Create Payment Intent Endpoint**
   ```python
   POST /api/stripe/create-payment-intent
   # Creates payment intent for monthly subscription
   # Returns client_secret for frontend
   ```

3. **Verify Payment Endpoint**
   ```python
   POST /api/stripe/verify-payment
   # Verifies payment was successful
   # Creates user account if payment verified
   ```

4. **Update Signup Endpoint**
   ```python
   POST /api/auth/signup
   # Now requires paymentIntentId parameter
   # Creates account only after payment verification
   ```

### Step 3: Frontend Changes

The `LoginSignup.jsx` component already has placeholders for Stripe integration.

**What needs to be added:**

1. **Payment Step Component**
   ```jsx
   // New component: PaymentStep.jsx
   - Stripe Elements wrapper
   - Payment form (card details)
   - Monthly subscription info display
   - Error handling
   ```

2. **Update Signup Flow**
   ```jsx
   // In LoginSignup.jsx
   1. User fills signup form
   2. Show payment step (after form validation)
   3. Create payment intent with backend
   4. Show Stripe payment form
   5. Process payment
   6. On success: call signup with paymentIntentId
   7. Auto-login user
   ```

3. **State Management**
   ```jsx
   const [showPayment, setShowPayment] = useState(false);
   const [paymentIntentId, setPaymentIntentId] = useState(null);
   const [clientSecret, setClientSecret] = useState(null);
   ```

### Step 4: Environment Variables

**Frontend `.env`:**
```env
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_...
VITE_STRIPE_PRICE_ID=price_... # Monthly subscription price ID
```

**Backend `.env`:**
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID=price_... # Monthly subscription price ID
```

## 🔧 Code Structure (To Be Implemented)

### PaymentStep Component Structure

```jsx
// components/PaymentStep.jsx
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';

const PaymentStep = ({ onPaymentSuccess, onCancel, clientSecret }) => {
  // Stripe payment form implementation
  // Handle payment submission
  // Return paymentIntentId on success
};
```

### Updated Signup Flow

```jsx
// In LoginSignup.jsx
const handleSignup = async () => {
  // 1. Validate form
  // 2. Create payment intent with backend
  const response = await fetch('/api/stripe/create-payment-intent', {
    method: 'POST',
    body: JSON.stringify({ email, username })
  });
  const { clientSecret } = await response.json();
  
  // 3. Show payment form
  setShowPayment(true);
  setClientSecret(clientSecret);
  
  // 4. After payment success in PaymentStep:
  // - Get paymentIntentId
  // - Call signup with paymentIntentId
  // - Auto-login
};
```

## 💰 Subscription Details

- **Price:** TBD (e.g., $9.99/month)
- **Billing:** Monthly recurring
- **Plan:** Single tier (can expand later)

## 🔐 Security Considerations

1. **Never expose Stripe secret key** in frontend
2. **Verify payment on backend** before creating account
3. **Use webhooks** for payment status updates
4. **Validate paymentIntentId** on signup endpoint
5. **Handle payment failures** gracefully

## 📝 Testing

Use Stripe test cards:
- **Success:** `4242 4242 4242 4242`
- **Decline:** `4000 0000 0000 0002`
- **3D Secure:** `4000 0027 6000 3184`

Any future date for expiry, any 3 digits for CVC.

## 🚀 Migration Path

Current signup flow (mock):
```
Form → Signup → Login
```

Future signup flow (with Stripe):
```
Form → Create Payment Intent → Payment Form → Verify Payment → Signup → Login
```

The code is structured to make this transition smooth!

---

**Status:** ⏳ Ready for implementation when backend is set up



