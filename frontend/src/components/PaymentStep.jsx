import React, { useState } from 'react';
import { loadStripe } from '@stripe/stripe-js';
import {
  Elements,
  CardElement,
  useStripe,
  useElements
} from '@stripe/react-stripe-js';
import '../styles/PaymentStep.css';

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || '');

const PaymentForm = ({ amount, onSuccess, onCancel, clientSecret }) => {
  const stripe = useStripe();
  const elements = useElements();
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!stripe || !elements) {
      return;
    }

    setProcessing(true);
    setError(null);

    const cardElement = elements.getElement(CardElement);

    try {
      const { error: stripeError, paymentIntent } = await stripe.confirmCardPayment(
        clientSecret,
        {
          payment_method: {
            card: cardElement,
          }
        }
      );

      if (stripeError) {
        setError(stripeError.message);
        setProcessing(false);
      } else if (paymentIntent && paymentIntent.status === 'succeeded') {
        onSuccess(paymentIntent.id);
      }
    } catch (err) {
      setError('Payment failed. Please try again.');
      setProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="payment-form">
      <div className="payment-info">
        <h3>Monthly Subscription</h3>
        <p className="payment-amount">${amount}/month</p>
        <p className="payment-description">
          Billed monthly. Cancel anytime.
        </p>
      </div>

      <div className="card-element-container">
        <label>Card Details</label>
        <CardElement
          options={{
            style: {
              base: {
                fontSize: '16px',
                color: '#ffffff',
                '::placeholder': {
                  color: '#888',
                },
              },
              invalid: {
                color: '#ff6b6b',
              },
            },
          }}
        />
      </div>

      {error && <div className="payment-error">{error}</div>}

      <div className="payment-buttons">
        <button
          type="button"
          className="cancel-payment-button"
          onClick={onCancel}
          disabled={processing}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="submit-payment-button"
          disabled={!stripe || processing}
        >
          {processing ? 'Processing...' : `Pay $${amount}`}
        </button>
      </div>

      <p className="payment-note">
        Test card: 4242 4242 4242 4242 | Any future date | Any 3 digits
      </p>
    </form>
  );
};

const PaymentStep = ({ amount = 9.99, onPaymentSuccess, onCancel }) => {
  const [clientSecret, setClientSecret] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  React.useEffect(() => {
    // Create payment intent
    const createPaymentIntent = async () => {
      try {
        const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
        const response = await fetch(`${API_BASE_URL}/api/stripe/create-payment-intent`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });

        if (!response.ok) {
          throw new Error('Failed to create payment intent');
        }

        const data = await response.json();
        setClientSecret(data.client_secret);
      } catch (err) {
        setError('Failed to initialize payment. Please try again.');
        console.error('Payment intent error:', err);
      } finally {
        setLoading(false);
      }
    };

    createPaymentIntent();
  }, []);

  if (loading) {
    return (
      <div className="payment-loading">
        <div className="spinner"></div>
        <p>Initializing payment...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="payment-error-container">
        <p>{error}</p>
        <button onClick={onCancel}>Go Back</button>
      </div>
    );
  }

  if (!clientSecret) {
    return (
      <div className="payment-error-container">
        <p>Payment initialization failed</p>
        <button onClick={onCancel}>Go Back</button>
      </div>
    );
  }

  return (
    <div className="payment-step-container">
      <Elements stripe={stripePromise}>
        <PaymentForm
          amount={amount}
          clientSecret={clientSecret}
          onSuccess={onPaymentSuccess}
          onCancel={onCancel}
        />
      </Elements>
    </div>
  );
};

export default PaymentStep;

