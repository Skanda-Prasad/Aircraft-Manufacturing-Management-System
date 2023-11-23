document.addEventListener("DOMContentLoaded", function () {
    // Function to open a dialog by its ID
    function openDialog(dialogId) {
        const dialog = document.getElementById(dialogId);
        dialog.style.display = "block";
    }

    // Function to close a dialog by its ID
    function closeDialog(dialogId) {
        const dialog = document.getElementById(dialogId);
        dialog.style.display = "none";
    }
    
    
      // Add event listeners for opening dialog boxes
  document.getElementById("create-aircraft-model").addEventListener("click", () => openDialog("create-aircraft-model-dialog"));
  document.getElementById("create-aircraft-component").addEventListener("click", () => openDialog("create-aircraft-component-dialog"));
  document.getElementById("create-supplier").addEventListener("click", () => openDialog("create-supplier-dialog"));
  document.getElementById("create-employee").addEventListener("click", () => openDialog("create-employee-dialog"));
  document.getElementById("create-production-line").addEventListener("click", () => openDialog("create-production-line-dialog"));
  document.getElementById("create-aircraft-order").addEventListener("click", () => openDialog("create-aircraft-order-dialog"));
  document.getElementById("create-customer").addEventListener("click", () => openDialog("create-customer-dialog"));

  // Add event listeners for closing dialog boxes
  document.getElementById("cancel-model").addEventListener("click", () => closeDialog("create-aircraft-model-dialog"));
  document.getElementById("cancel-component").addEventListener("click", () => closeDialog("create-aircraft-component-dialog"));
  document.getElementById("cancel-supplier").addEventListener("click", () => closeDialog("create-supplier-dialog"));
  document.getElementById("cancel-employee").addEventListener("click", () => closeDialog("create-employee-dialog"));
  document.getElementById("cancel-production-line").addEventListener("click", () => closeDialog("create-production-line-dialog"));
  document.getElementById("cancel-aircraft-order").addEventListener("click", () => closeDialog("create-aircraft-order-dialog"));
  document.getElementById("cancel-customer").addEventListener("click", () => closeDialog("create-customer-dialog"));

    // Add event listener for logout
    document.getElementById("logout").addEventListener("click", () => logout());

    function logout() {
        window.location.href = "login.html"; 
    }
});



document.addEventListener('DOMContentLoaded', function () {
    // Buttons
    const viewUsersButton = document.getElementById('view-users');
    const viewAircraftModelsButton = document.getElementById('view-aircraft-models');
    const viewAircraftComponentsButton = document.getElementById('view-aircraft-components');
    const viewSuppliersButton = document.getElementById('view-suppliers');
    const viewEmployeesButton = document.getElementById('view-employees');
    const viewProductionLinesButton = document.getElementById('view-production-lines');
    const viewAircraftOrdersButton = document.getElementById('view-aircraft-orders');
    const viewCustomersButton = document.getElementById('view-customers');
    const viewComponentInventoryButton = document.getElementById('view-component-inventory');

    // Table containers
    const userTable = document.getElementById('user-table');
    const aircraftModelTable = document.getElementById('aircraft-model-table');
    const aircraftComponentTable = document.getElementById('aircraft-component-table');
    const supplierTable = document.getElementById('supplier-table');
    const employeeTable = document.getElementById('employee-table');
    const productionLineTable = document.getElementById('production-line-table');
    const aircraftOrderTable = document.getElementById('aircraft-order-table');
    const customerTable = document.getElementById('customer-table');
    const componentInventoryTable = document.getElementById('component-inventory-table');

    // Event listeners for buttons
    viewUsersButton.addEventListener('click', () => fetchDataAndDisplay('users', userTable));
    viewAircraftModelsButton.addEventListener('click', () => fetchDataAndDisplay('aircraft_model', aircraftModelTable));
    viewAircraftComponentsButton.addEventListener('click', () => fetchDataAndDisplay('aircraft_component', aircraftComponentTable));
    viewSuppliersButton.addEventListener('click', () => fetchDataAndDisplay('supplier', supplierTable));
    viewEmployeesButton.addEventListener('click', () => fetchDataAndDisplay('employee', employeeTable));
    viewProductionLinesButton.addEventListener('click', () => fetchDataAndDisplay('production_line', productionLineTable));
    viewAircraftOrdersButton.addEventListener('click', () => fetchDataAndDisplay('aircraft_order', aircraftOrderTable));
    viewCustomersButton.addEventListener('click', () => fetchDataAndDisplay('customer', customerTable));
    viewComponentInventoryButton.addEventListener('click', () => fetchDataAndDisplay('component_inventory', componentInventoryTable));
});

function fetchDataAndDisplay(tableName, tableContainer) {
    // Fetch data from the server
    fetch(`/get_${tableName}_data`) // Replace with your actual endpoint
        .then(response => response.json())
        .then(data => {
            displayTableData(tableName, data, tableContainer);
        })
        .catch(error => {
            console.error(`Error fetching data for ${tableName}:`, error);
        });
}

function displayTableData(tableName, tableData, tableContainer) {
    // Clear existing table content
    tableContainer.innerHTML = '';

    // Create a new table element
    const tableElement = document.createElement('table');
    tableElement.border = '1';

    // Create header row
    const headerRow = document.createElement('tr');
    Object.keys(tableData[0]).forEach(header => {
        const th = document.createElement('th');
        th.textContent = header;
        headerRow.appendChild(th);
    });
    tableElement.appendChild(headerRow);

    // Populate table with data
    tableData.forEach(rowData => {
        const row = document.createElement('tr');
        Object.values(rowData).forEach(value => {
            const cell = document.createElement('td');
            cell.textContent = value;
            row.appendChild(cell);
        });
        tableElement.appendChild(row);
    });

    // Append the table to the container
    tableContainer.appendChild(tableElement);
}




  // Add event listener for logout
  document.getElementById("logout").addEventListener("click", () => logout());

  function logout() {
    window.location.href = "login.html";
  }
});

