import React from 'react';
import { useSelector } from 'react-redux';

const CustomerTab = () => {
  const customer = useSelector(state => state.customer);

  return (
    <div className="p-4 table-container">
      <h2 className="text-xl font-bold mb-4">Customer Details</h2>
      <table className="min-w-full border-collapse border border-gray-200">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2">Customer Name</th>
            <th className="border p-2">Phone Number</th>
            <th className="border p-2">Total Purchase Amount</th>
          </tr>
        </thead>
        <tbody>
          {customer ? (
            <tr>
              <td className="border p-2">{customer.CustomerName}</td>
              <td className="border p-2">{customer.PhoneNumber}</td>
              <td className="border p-2">{customer.TotalPurchaseAmount.toFixed(2)}</td>
            </tr>
          ) : (
            <tr>
              <td className="border p-2 no-data-message" colSpan="3">No customer data available. Please upload an invoice file to see the details.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default CustomerTab;
