import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { updateProduct, deleteProduct } from '../store/actions';

const ProductsTab = () => {
  const products = useSelector(state => state.products);
  const dispatch = useDispatch();
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({});

  const handleEdit = (index, product) => {
    setEditingId(index);
    setEditForm(product);
  };

  const handleSave = (index) => {
    dispatch(updateProduct(index, editForm));
    setEditingId(null);
  };

  const handleDelete = (index) => {
    dispatch(deleteProduct(index));
  };

  return (
    <div className="p-4 table-container">
      <h2 className="text-xl font-bold mb-4">Products</h2>
      <table className="min-w-full border-collapse border border-gray-200">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2">Name</th>
            <th className="border p-2">Quantity</th>
            <th className="border p-2">Unit Price</th>
            <th className="border p-2">Tax</th>
            <th className="border p-2">Price With Tax</th>
            <th className="border p-2">Discount</th>
            <th className="border p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product, index) => (
            <tr key={index}>
              {editingId === index ? (
                <>
                  <td className="border p-2">
                    <input
                      type="text"
                      value={editForm.Name}
                      onChange={(e) => setEditForm({...editForm, Name: e.target.value})}
                      className="w-full p-1 border rounded"
                    />
                  </td>
                  <td className="border p-2">
                    <input
                      type="number"
                      value={editForm.Quantity}
                      onChange={(e) => setEditForm({...editForm, Quantity: Number(e.target.value)})}
                      className="w-full p-1 border rounded"
                    />
                  </td>
                  <td className="border p-2">
                    <input
                      type="number"
                      value={editForm.UnitPrice}
                      onChange={(e) => setEditForm({...editForm, UnitPrice: Number(e.target.value)})}
                      className="w-full p-1 border rounded"
                    />
                  </td>
                  <td className="border p-2">
                    <input
                      type="number"
                      value={editForm.Tax}
                      onChange={(e) => setEditForm({...editForm, Tax: Number(e.target.value)})}
                      className="w-full p-1 border rounded"
                    />
                  </td>
                  <td className="border p-2">
                    <input
                      type="number"
                      value={editForm.PriceWithTax}
                      onChange={(e) => setEditForm({...editForm, PriceWithTax: Number(e.target.value)})}
                      className="w-full p-1 border rounded"
                    />
                  </td>
                  <td className="border p-2">
                    <input
                      type="number"
                      value={editForm.Discount}
                      onChange={(e) => setEditForm({...editForm, Discount: Number(e.target.value)})}
                      className="w-full p-1 border rounded"
                    />
                  </td>
                  <td className="border p-2">
                    <button
                      onClick={() => handleSave(index)}
                      className="bg-green-500 text-white px-2 py-1 rounded mr-2"
                    >
                      Save
                    </button>
                  </td>
                </>
              ) : (
                <>
                  <td className="border p-2">{product.Name}</td>
                  <td className="border p-2">{product.Quantity}</td>
                  <td className="border p-2">{product.UnitPrice.toFixed(2)}</td>
                  <td className="border p-2">{product.Tax.toFixed(2)}</td>
                  <td className="border p-2">{product.PriceWithTax.toFixed(2)}</td>
                  <td className="border p-2">{product.Discount.toFixed(2)}</td>
                  <td className="border p-2">
                    <button
                      onClick={() => handleEdit(index, product)}
                      className="bg-blue-500 text-white px-2 py-1 rounded mr-2"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(index)}
                      className="bg-red-500 text-white px-2 py-1 rounded"
                    >
                      Delete
                    </button>
                  </td>
                </>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProductsTab;
