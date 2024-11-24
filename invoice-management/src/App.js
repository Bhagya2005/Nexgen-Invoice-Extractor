import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { setInvoiceData } from './store/actions';
import InvoiceTab from './components/InvoiceTab';
import ProductsTab from './components/ProductsTab';
import CustomerTab from './components/CustomerTab';
import './App.css';

const App = () => {
  const [activeTab, setActiveTab] = useState('invoice');
  const [processingMessage, setProcessingMessage] = useState('');
  const [isUploadDisabled, setIsUploadDisabled] = useState(false);
  const dispatch = useDispatch();
  
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setProcessingMessage('Processing your file, please wait...');
    setIsUploadDisabled(true);
    setTimeout(() => setProcessingMessage('Our AI system, is working on it!'), 4000);
    setTimeout(() => setProcessingMessage('Just SWIPE across tabs to see fields'), 8000);
    setTimeout(() => setProcessingMessage('Your output is on its way!'), 12000);
    setTimeout(() => setProcessingMessage('Hold tight!'), 16000);

    try {
      const response = await fetch('http://127.0.0.1:8000/process-invoice/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to process invoice');

      const data = await response.json();
      dispatch(setInvoiceData(data));
      setProcessingMessage('Completed Extraction!');

    } catch (error) {
      console.error('Error processing invoice:', error);
      alert('Failed to process invoice');
      setProcessingMessage('');
      setIsUploadDisabled(false);
    }
  };

  return (
    <div className="container">
      <h1 className="header">Invoice Management System</h1>
      
      <div className="file-upload">
        <label className={`button ${isUploadDisabled ? 'disabled' : ''}`}>
          <span className="icon">📁</span>
          Upload Invoice
          <input type="file" onChange={handleFileUpload} disabled={isUploadDisabled} />
        </label>
      </div>

      {processingMessage && <div className="processing-message">{processingMessage}</div>}

      <div className="navbar">
        <div
          onClick={() => setActiveTab('invoice')}
          className={`tab ${activeTab === 'invoice' ? 'active' : ''}`}
        >
          Invoice
        </div>
        <div
          onClick={() => setActiveTab('products')}
          className={`tab ${activeTab === 'products' ? 'active' : ''}`}
        >
          Products
        </div>
        <div
          onClick={() => setActiveTab('customer')}
          className={`tab ${activeTab === 'customer' ? 'active' : ''}`}
        >
          Customer
        </div>
      </div>

      {activeTab === 'invoice' && <InvoiceTab />}
      {activeTab === 'products' && <ProductsTab />}
      {activeTab === 'customer' && <CustomerTab />}
    </div>
  );
};

export default App;