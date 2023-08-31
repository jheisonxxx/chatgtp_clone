import React, { Component } from 'react';

class FileUploadForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      apiKey: '',
      selectedFile: null,
      response: '',
    };
  }

  handleApiKeyChange = (event) => {
    this.setState({ apiKey: event.target.value });
  };

  handleFileChange = (event) => {
    this.setState({ selectedFile: event.target.files[0] });
  };

  handleUpload = () => {
    const { apiKey, selectedFile } = this.state;

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('apikey', apiKey);

    fetch('http://localhost:9000/api/v1/chatgtp/upload-file', {
      method: 'POST',
      body: formData,
      headers: {
      },
    })
      .then((response) => response.json())
      .then((data) => {
        this.setState({ response: JSON.stringify(data) });
      })
      .catch((error) => {
        console.error('Error uploading file:', error);
      });
  };

  render() {
    return (
      <div className='container'>
      <div className='row'>
      <div className='col-md-12 my-2' class="text-center">
        <h1>
          CSV <span>interpretation</span>
        </h1>
       </div>
       <div className='col-md-12 my-2'>
        <h2>
          {" "}
          Upload a csv file and you will receive an analysis of the data
        </h2>
      </div>
      </div>
      <div>
        <div>
            <div class="row g-3 align-items-center">
                <div class="col-auto">
                    <label for="apikey" class="col-form-label">API Key</label>
                </div>
                <div class="col-auto">
                <input type="text" class="form-control" required value={this.state.apiKey} onChange={this.handleApiKeyChange}/>
                </div>
            </div>
            <div class="row g-3 align-items-center my-2">
                <div class="col-auto">
                    <label for="select_file" class="col-form-label">Select a file:</label>
                </div>
                <div class="col-auto">
                <input type="file" required class="form-control" name="file" onChange={this.handleFileChange} />
                </div>
            </div>
            <div class="row g-3 align-items-center">
                <div class="col-auto">
                <button className='btn btn-primary mt-3 mb-3' onClick={this.handleUpload}>Upload CSV</button>
                </div>
            </div>
        </div>
        <div>
          <h3>Analysis</h3>
          <textarea
            className='form-control'
            placeholder="Here is the analysis"
            cols={80}
            rows={14}
            value={this.state.response}
          />
        </div>
      </div>
    </div>
    );
  }
}

export default FileUploadForm;