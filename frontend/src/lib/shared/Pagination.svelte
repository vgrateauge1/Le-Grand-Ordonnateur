<script lang="ts">
    export let currentPage: number = 1; // Current page number
    export let pageSize: number = 2; // Number of items per page
    export let totalItems: number = 0; // Total number of items
    export let onPageChange: (page: number) => void; // Callback for page change
  
    // Calculate total pages dynamically
    $: totalPages = Math.ceil(totalItems / pageSize);
  
    // Handlers for button clicks
    const goToPreviousPage = () => {
      if (currentPage > 1) {
        onPageChange(currentPage - 1); // Trigger callback for previous page
      }
    };
  
    const goToNextPage = () => {
      if (currentPage < totalPages) {
        onPageChange(currentPage + 1); // Trigger callback for next page
      }
    };
  </script>
  
  <div class="pagination">
    <!-- Previous Button -->
    <button on:click={goToPreviousPage} disabled={currentPage <= 1}>
      Previous
    </button>
  
    <!-- Page Indicator -->
    <span>Page {currentPage} of {totalPages}</span>
  
    <!-- Next Button -->
    <button on:click={goToNextPage} disabled={currentPage >= totalPages}>
      Next
    </button>
  </div>
  
  <style>
    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-top: 1em;
      gap: 1em;
    }
  
    button {
      padding: 0.5em 1em;
      background: #007bff;
      color: #fff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  
    button:disabled {
      background: #ccc;
      cursor: not-allowed;
    }
  </style>
  