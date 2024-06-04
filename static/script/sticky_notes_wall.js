
function Main() {
    const svg = document.getElementById('sticky-notes-7'); // Ensure the ID matches your SVG element
    if (svg) {
      svg.style.fill = "#ffffff"; // This changes the fill color to white
      console.log("Color change happened!");
    } else {
      console.log("SVG not found!");
    }
  }
  
  
window.onload = () => {
    Main();
};


// document.addEventListener('DOMContentLoaded', function() {

//     Main();
  
  
//   });