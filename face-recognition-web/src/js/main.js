// Simulate transitions between Face Recognition and Voice Recognition
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
      document.getElementById('face-recognition').style.display = 'none';
      document.getElementById('voice-recognition').style.display = 'flex';
    }, 5000); // Simulate 5 seconds for face recognition
  });
  
