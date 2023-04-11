      const resetText = document.querySelector(".title-text .reset");
      const resetForm = document.querySelector("form.reset");
      const resetBtn = document.querySelector("label.reset");
      resetBtn.onclick = (()=>{
        resetForm.style.marginLeft = "-50%";
        resetText.style.marginLeft = "-50%";
      });
      resetBtn.onclick = (()=>{
        resetForm.style.marginLeft = "0%";
        resetText.style.marginLeft = "0%";
      });