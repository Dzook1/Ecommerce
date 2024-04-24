function productDivPopUp(){
    filter = document.getElementsByClassName('filter')[0];
    filter.style.display = 'none';
    productGrid = document.getElementsByClassName('productGrid')[0];
    productGrid.style.display = 'none';

    productDiv = document.getElementsByClassName('productDiv')[0];
    productDiv.style.display = 'block';
}

function backToProductGrid(){
    productDiv = document.getElementsByClassName('productDiv')[0];
    productDiv.style.display = 'none';

    filter = document.getElementsByClassName('filter')[0];
    filter.style.display = 'block';
    productGrid = document.getElementsByClassName('productGrid')[0];
    productGrid.style.display = 'grid';
}
