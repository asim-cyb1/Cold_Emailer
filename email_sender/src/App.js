import React, { useState } from 'react';
import axios from 'axios';

export default function JobEmailApp() {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [generatedEmail, setGeneratedEmail] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  const handleGenerateEmail = async () => {
    try {
      const formData = new FormData();
      formData.append('job_description', jobDescription);

      const response = await axios.post('http://localhost:8000/generate-email', formData);
      setGeneratedEmail(response.data.email);
    } catch (error) {
      console.error('Error generating email:', error);
    }
  };

  const handleSendEmail = async () => {
    if (!resumeFile) {
      setStatusMessage('Please upload a resume before sending.');
      return;
    }
    try {
      const formData = new FormData();
      formData.append('job_description', jobDescription);
      formData.append('resume', resumeFile);

      const response = await axios.post('http://localhost:8000/send-email', formData);
      setStatusMessage(response.data.status);
    } catch (error) {
      console.error('Error sending email:', error);
      setStatusMessage('Error sending email.');
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold text-center">Job Email Generator</h1>

      <textarea
        className="w-full p-2 border rounded"
        rows="8"
        placeholder="Paste job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      ></textarea>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setResumeFile(e.target.files[0])}
        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
      />

      <div className="flex gap-4">
        <button
          onClick={handleGenerateEmail}
          className="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded"
        >
          Generate Email
        </button>

        <button
          onClick={handleSendEmail}
          className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded"
        >
          Send Email
        </button>
      </div>

      {generatedEmail && (
        <div className="mt-4 p-4 border rounded bg-gray-50">
          <h2 className="font-semibold">Generated Email:</h2>
          <p className="whitespace-pre-wrap mt-2">{generatedEmail}</p>
        </div>
      )}

      {statusMessage && (
        <div className="mt-4 text-blue-700 font-medium">
          {statusMessage}
        </div>
      )}
    </div>
  );
}
