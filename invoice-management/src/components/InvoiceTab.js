import React from 'react';
import { useSelector } from 'react-redux';

const InvoiceTab = () => {
  const invoice = useSelector(state => state.invoice);

  return (
    <div className="p-4 table-container">
      <h2 className="text-xl font-bold mb-4">Invoice Details</h2>
      <table className="min-w-full border-collapse border border-gray-200">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2">Serial Number</th>
            <th className="border p-2">Customer Name</th>
            <th className="border p-2">Quantity</th>
            <th className="border p-2">Total Tax</th>
            <th className="border p-2">Total Amount</th>
            <th className="border p-2">Date</th>
          </tr>
        </thead>
        <tbody>
          {invoice ? (
            <tr>
              <td className="border p-2">{invoice.SerialNumber}</td>
              <td className="border p-2">{invoice.CustomerName}</td>
              <td className="border p-2">{invoice.Quantity}</td>
              <td className="border p-2">{invoice.TotalTax.toFixed(2)}</td>
              <td className="border p-2">{invoice.TotalAmount.toFixed(2)}</td>
              <td className="border p-2">{invoice.Date}</td>
            </tr>
          ) : (
            <tr>
              <td className="border p-2 no-data-message" colSpan="6">No invoices uploaded yet! Click the button above to get started.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default InvoiceTab;