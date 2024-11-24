import { UPDATE_PRODUCT, DELETE_PRODUCT, SET_INVOICE_DATA } from './types';

export const updateProduct = (productId, updatedProduct) => ({
  type: UPDATE_PRODUCT,
  payload: { productId, updatedProduct }
});

export const deleteProduct = (productId) => ({
  type: DELETE_PRODUCT,
  payload: productId
});

export const setInvoiceData = (data) => ({
  type: SET_INVOICE_DATA,
  payload: data
});