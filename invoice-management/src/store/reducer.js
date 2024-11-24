import { UPDATE_PRODUCT, DELETE_PRODUCT, SET_INVOICE_DATA } from './types';

const initialState = {
  invoice: null,
  products: [],
  customer: null
};

const calculateTotals = (products) => {
  return products.reduce((acc, product) => ({
    quantity: acc.quantity + product.Quantity,
    totalTax: acc.totalTax + product.Tax,
    totalAmount: acc.totalAmount + product.PriceWithTax
  }), { quantity: 0, totalTax: 0, totalAmount: 0 });
};

export const invoiceReducer = (state = initialState, action) => {
  switch (action.type) {
    case SET_INVOICE_DATA:
      return {
        ...state,
        invoice: action.payload.Invoice,
        products: action.payload.Products,
        customer: action.payload.Customer
      };

    case UPDATE_PRODUCT:
      const updatedProducts = state.products.map((product, index) => 
        index === action.payload.productId ? action.payload.updatedProduct : product
      );
      const newTotals = calculateTotals(updatedProducts);
      
      return {
        ...state,
        products: updatedProducts,
        invoice: {
          ...state.invoice,
          Quantity: newTotals.quantity,
          TotalTax: newTotals.totalTax,
          TotalAmount: newTotals.totalAmount
        },
        customer: {
          ...state.customer,
          TotalPurchaseAmount: newTotals.totalAmount
        }
      };

    case DELETE_PRODUCT:
      const productsAfterDelete = state.products.filter((_, index) => 
        index !== action.payload
      );
      const totalsAfterDelete = calculateTotals(productsAfterDelete);

      return {
        ...state,
        products: productsAfterDelete,
        invoice: {
          ...state.invoice,
          Quantity: totalsAfterDelete.quantity,
          TotalTax: totalsAfterDelete.totalTax,
          TotalAmount: totalsAfterDelete.totalAmount
        },
        customer: {
          ...state.customer,
          TotalPurchaseAmount: totalsAfterDelete.totalAmount
        }
      };

    default:
      return state;
  }
};