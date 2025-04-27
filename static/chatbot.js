let conversationState = null; 

function sendMessage() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");
  const message = input.value.trim();
  if (!message) return;

  const userDiv = document.createElement("div");
  userDiv.className = "user-message ms-auto";
  userDiv.innerText = message;
  chatBox.appendChild(userDiv);

  const botDiv = document.createElement("div");
  botDiv.className = "bot-message me-auto";
  botDiv.innerText = getBotResponse(message);
  chatBox.appendChild(botDiv);

  chatBox.scrollTop = chatBox.scrollHeight;
  input.value = "";
}

function getBotResponse(message) {
  const lang = document.documentElement.lang; 
  const lowerMessage = message.toLowerCase();

  if (lang === "ar") {
    if (lowerMessage.includes("بلاغ") || lowerMessage.includes("فقدت") || lowerMessage.includes("ضاع")) {
      return "يؤسفني سماع ذلك. لرفع بلاغ:\n1- سجل دخولك إلى حسابك.\n2- اضغط على زر (إبلاغ عن غرض مفقود).\n3- عبئ النموذج بالمعلومات المطلوبة.\n4- اضغط إرسال.";
    } else if (lowerMessage.includes("مساعدة") || lowerMessage.includes("مشكلة") || lowerMessage.includes("دعم")) {
      return "للمساعدة، يمكنك التواصل مع الدعم الفني عبر صفحة التواصل، أو مراجعة قسم الأسئلة الشائعة.";
    } else if (lowerMessage.includes("كيف") || lowerMessage.includes("طريقة")) {
      return "لرفع بلاغ: سجل دخولك ➔ اضغط على (إبلاغ عن غرض مفقود) ➔ املأ النموذج ➔ اضغط إرسال.";
    } else {
      return "عذرًا، لم أفهم سؤالك تمامًا. حاول استخدام كلمات مثل بلاغ، مساعدة، دعم.";
    }
  } else {
    if (lowerMessage.includes("report") || lowerMessage.includes("lost") || lowerMessage.includes("missing")) {
      return "I'm sorry to hear that. To submit a report:\n1- Log in to your account.\n2- Click on (Report a Lost Item).\n3- Fill in the required form.\n4- Click submit.";
    } else if (lowerMessage.includes("help") || lowerMessage.includes("support") || lowerMessage.includes("problem")) {
      return "For help, please contact our support team through the contact page or check the FAQ section.";
    } else if (lowerMessage.includes("how") || lowerMessage.includes("way")) {
      return "To report a lost item: Log in ➔ Click (Report a Lost Item) ➔ Fill the form ➔ Submit.";
    } else {
      return "Sorry, I didn't fully understand. Try using words like report, help, or support.";
    }
  }
}

function newChat() {
  conversationState = null; 
  document.getElementById("chatBox").innerHTML = "";
}
