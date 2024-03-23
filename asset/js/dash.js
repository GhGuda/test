const navItems = document.querySelectorAll(".nav-item");

navItems.forEach((navItem, i) => {
  navItem.addEventListener("click", () => {
    navItems.forEach((item, j) => {
      item.className = "nav-item";
    });
    navItem.className = "nav-item active";
  });
});






document.addEventListener('DOMContentLoaded', function () {
    const lightIcon = document.getElementById('light-icon');
    const darkIcon = document.getElementById('dark-icon');
    const body = document.body;
  
    // Check for saved mode in local storage
    const savedMode = localStorage.getItem('mode');

    if (savedMode === 'dark-mode') {
      body.classList.add('dark-mode');
      // Show the moon icon when in dark mode
      darkIcon.style.display = 'inline';
      lightIcon.style.display = 'none';
    } else {
      // Show the lightbulb icon when in light mode
      lightIcon.style.display = 'inline';
      darkIcon.style.display = 'none';
    }
  
    // Toggle between dark and light mode
    lightIcon.addEventListener('click', toggleMode);
    darkIcon.addEventListener('click', toggleMode);
  
    function toggleMode() {
      body.classList.toggle('dark-mode');
      const newMode = body.classList.contains('dark-mode') ? 'dark-mode' : 'light-mode';
      localStorage.setItem('mode', newMode);
      // Toggle visibility of icons
      lightIcon.style.display = body.classList.contains('dark-mode') ? 'none' : 'inline';
      darkIcon.style.display = body.classList.contains('dark-mode') ? 'inline' : 'none';
    }
  });







  
  // Function to show or hide input fields based on selected option
function toggleInputFields() {
  var selectedOption = document.getElementById("paymentMethod").value;
  
  // Hide all input fields initially
  document.getElementById("bankFields").style.display = "none";
  document.getElementById("momoFields").style.display = "none";
  
  // Show input fields based on selected option
  if (selectedOption === "bank") {
      document.getElementById("bankFields").style.display = "block";
  } else if (selectedOption === "momo") {
      document.getElementById("momoFields").style.display = "block";
  }
}

// Add event listener to the dropdown to trigger the function when an option is selected
document.getElementById("paymentMethod").addEventListener("change", toggleInputFields);

// Call the function initially to ensure correct display based on the default selected option
toggleInputFields();





// List of banks in Ghana
const banksInGhana = [
  "Access Bank",
  "Agricultural Development Bank (ADB)",
  "Bank of Africa",
  "Barclays Bank Ghana",
  "CalBank",
  "Ecobank Ghana",
  "Fidelity Bank Ghana",
  "GCB Bank",
  "National Investment Bank (NIB)",
  "Republic Bank Ghana (formerly HFC Bank)",
  "Societe Generale Ghana",
  "Standard Chartered Bank Ghana",
  "Stanbic Bank Ghana",
  "United Bank for Africa (UBA)",
  "Zenith Bank Ghana"
  // Add more banks as needed
];

// Function to populate the select field with banks
function populateBankSelect() {
  const bankSelect = document.getElementById("bankSelect");
  
  // Loop through the banks array and create an option element for each bank
  banksInGhana.forEach((bank, index) => {
      const option = document.createElement("option");
      option.value = index + 1; // Assigning unique value for each bank
      option.textContent = bank;
      bankSelect.appendChild(option);
      
      // If Zenith Bank Ghana is reached, add the "Other" option
      if (bank === "Zenith Bank Ghana") {
          const otherOption = document.createElement("option");
          otherOption.value = "other";
          otherOption.textContent = "Other (Enter bank name)";
          bankSelect.appendChild(otherOption);
      }
  });
}

// Call the function to populate the select field
populateBankSelect();

// Function to handle change event on the select field
document.getElementById("bankSelect").addEventListener("change", function() {
  const selectedBank = this.value;
  const otherBankInput = document.getElementById("otherBankInput");

  // If "Other" option is selected, show the input field
  if (selectedBank === "other") {
      otherBankInput.style.display = "block";
  } else {
      otherBankInput.style.display = "none";
  }
});



// Function to show or hide payment method fields based on selected option
function togglePaymentMethodFields() {
  const paymentMethod = document.getElementById("paymentMethod").value;
  const bankFields = document.getElementById("bankFields");
  const momoFields = document.getElementById("momoFields");

  // If the selected option is the default one, hide the payment method fields
  if (paymentMethod === "default") {
      bankFields.style.display = "none";
      momoFields.style.display = "none";
  } else {
      // Otherwise, show the appropriate payment method fields
      if (paymentMethod === "bank") {
          bankFields.style.display = "block";
          momoFields.style.display = "none";
      } else if (paymentMethod === "momo") {
          momoFields.style.display = "block";
          bankFields.style.display = "none";
      }
  }
}

// Attach change event listener to the payment method dropdown
document.getElementById("paymentMethod").addEventListener("change", togglePaymentMethodFields);

// Call the function to initially set the display of payment method fields
togglePaymentMethodFields();






//Payout
function calculatePayout() {
  // Get the gift card amount entered by the user
  const giftCardAmount = parseFloat(document.getElementById("giftCardAmount").value);
  
  // Check if the input is a valid number
  if (!isNaN(giftCardAmount)) {
      // Perform your calculation here (for example, multiplying by a fixed rate)
      const payoutAmount = giftCardAmount * 13; // Example: 90% payout rate
      
      // Update the payout details input field with the calculated amount
      document.getElementById("payoutDetails").value = payoutAmount.toFixed(1);
  } else {
      // If the input is not a valid number, clear the payout details field
      document.getElementById("payoutDetails").value = "";
  }
}

// Attach input event listener to the gift card amount field
document.getElementById("giftCardAmount").addEventListener("input", calculatePayout);

// Initial calculation when the page loads
calculatePayout();




//For Image Preview

document.getElementById('giftCardImage').addEventListener('change', function(event) {
  const files = event.target.files;
  const imagePreview = document.getElementById('imagePreview');
  imagePreview.innerHTML = ''; // Clear previous images

  // Loop through selected files
  for (let i = 0; i < files.length; i++) {
      const file = files[i];
      
      // Only display images
      if (!file.type.startsWith('image/')) {
          continue;
      }
      
      const reader = new FileReader();

      reader.onload = function() {
          // Create image element
          const img = document.createElement('img');
          img.src = reader.result;
          img.style.maxWidth = '100px'; // Limit image width for display
          img.style.maxHeight = '100px'; // Limit image height for display
          imagePreview.appendChild(img);
      }

      reader.readAsDataURL(file);
  }
});





document.addEventListener('DOMContentLoaded', function () {
  // Get references to the balance element and the emoji toggle element
  const balanceElement = document.getElementById("balance");
  const emojiToggleElement = document.getElementById("emojiToggle");

  // Add event listener to the emoji toggle element
  emojiToggleElement.addEventListener("click", function() {
      // Toggle the visibility of the balance element
      if (balanceElement.style.display === "none") {
          balanceElement.style.display = "block";
          emojiToggleElement.textContent = "💸💸💸"; // Change emoji to 💸💸💸 when balance is visible
      } else {
          balanceElement.style.display = "none";
          emojiToggleElement.textContent = "😑😑😑"; // Change emoji back to 😑😑😑 when balance is hidden
      }
  });
});
