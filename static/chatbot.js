function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  if (!message) return;
  addMessage(message, "user");
  input.value = "";

  showTypingIndicator();
  setTimeout(() => {
    hideTypingIndicator();
    handleBotResponse(message);
  }, 1000);
}

function addMessage(text, sender) {
  const chatBox = document.getElementById("chatInner");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender}-message`;
  messageDiv.innerText = text;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
  const chatBox = document.getElementById("chatInner");
  const typingDiv = document.createElement("div");
  typingDiv.className = "message bot-message";
  typingDiv.id = "typingIndicator";
  typingDiv.innerText = getLang() === "ar" ? "يكتب..." : "Typing...";
  chatBox.appendChild(typingDiv);
}

function hideTypingIndicator() {
  const typingDiv = document.getElementById("typingIndicator");
  if (typingDiv) typingDiv.remove();
}

function normalizeArabic(text) {
  return text.replace(/[أإآ]/g, 'ا');
}

function detectIntent(text) {
  const normalized = normalizeArabic(text.toLowerCase());

  if (normalized.includes("فقدت") || normalized.includes("ضاع") || normalized.includes("مفقود") || normalized.includes("ضيعت") || normalized.includes("اختفى") || normalized.includes("انسرق") || normalized.includes("غرض ضائع") || normalized.includes("غرض مفقود") || normalized.includes("lost") || normalized.includes("missing") || normalized.includes("stolen")) {
    return "lost_item";
  }

  if (normalized.includes("بحث") || normalized.includes("ابحث") || normalized.includes("ادور") || normalized.includes("استعلام") || normalized.includes("search") || normalized.includes("find item")) {
    return "search_item";
  }

  if (normalized.includes("كيف ابلغ") || normalized.includes("اريد تقديم بلاغ") || normalized.includes("اريد ابلغ") || normalized.includes("بلاغ") || normalized.includes("how to report") || normalized.includes("report")) {
    return "report_item";
  }

  if (normalized.includes("مساعدة") || normalized.includes("مشكلة") || normalized.includes("دعم") || normalized.includes("تعليق") || normalized.includes("بلاغ خطأ") || normalized.includes("help") || normalized.includes("support") || normalized.includes("problem")) {
    return "support";
  }

  if (normalized.includes("شكرا") || normalized.includes("مشكور") || normalized.includes("ثانكس") || normalized.includes("thanks") || normalized.includes("thank you") || normalized.includes("ممتاز") || normalized.includes("رائع")) {
    return "thanks";
  }

  if (normalized.includes("تواصل") || normalized.includes("رقم التواصل") || normalized.includes("اتصال") || normalized.includes("اتصل") || normalized.includes("contact") || normalized.includes("phone number") || normalized.includes("call")) {
    return "contact";
  }

  if (normalized.includes("موقعكم") || normalized.includes("مكانكم") || normalized.includes("اين مكانكم") || normalized.includes("location") || normalized.includes("where are you") || normalized.includes("address")) {
    return "location";
  }

  if (normalized.includes("ساعات العمل") || normalized.includes("وقت الدوام") || normalized.includes("متى فاتحين") || normalized.includes("اوقات العمل") || normalized.includes("working hours") || normalized.includes("open time")) {
    return "working_hours";
  }

  if (normalized.includes("تسجيل خروج") || normalized.includes("خروج") || normalized.includes("logout") || normalized.includes("sign out") || normalized.includes("انهاء الجلسة")) {
    return "logout";
  }

  if (normalized.includes("مين انت") || normalized.includes("من انت") || normalized.includes("وش تسوي") || normalized.includes("تعريفك") || normalized.includes("who are you") || normalized.includes("what do you do")) {
    return "who_are_you";
  }

  if (normalized.includes("حالة البلاغ") || normalized.includes("متابعة البلاغ") || normalized.includes("نتيجة البلاغ") || normalized.includes("status report") || normalized.includes("my report")) {
    return "report_status";
  }

  if (normalized.includes("سلام") || normalized.includes("هلا") || normalized.includes("اهلين") || normalized.includes("مرحبا") || normalized.includes("hello") || normalized.includes("hi") || normalized.includes("good morning") || normalized.includes("good evening")) {
    return "greeting";
  }

  if (normalized.includes("كيف حالك") || normalized.includes("شلونك") || normalized.includes("اخبارك") || normalized.includes("how are you") || normalized.includes("how's it going")) {
    return "how_are_you";
  }

  return "unknown";
}

function handleBotResponse(message) {
  const lang = getLang();
  const intent = detectIntent(message);

  if (intent === "lost_item") {
    return addMessage(lang === "ar" ? "😢 يؤسفني سماع ذلك. يمكنك رفع بلاغ عبر حسابك." : "😢 Sorry to hear that. You can submit a report through your account.", "bot");
  }

  if (intent === "search_item") {
    return addMessage(lang === "ar" ? "🔍 يمكنك البحث عن المفقودات عبر قسم البحث في حسابك." : "🔍 You can search for lost items through the search section in your account.", "bot");
  }

  if (intent === "report_item") {
    return addMessage(lang === "ar" ? "📝 لتقديم بلاغ: سجل دخولك واضغط على زر (رفع بلاغ)." : "📝 To report an item: Log in and click (Report Lost Item).", "bot");
  }

  if (intent === "support") {
    return addMessage(lang === "ar" ? "🤝 نحن هنا لمساعدتك! تواصل معنا عبر الدعم الفني." : "🤝 We're here to help! Contact our support team.", "bot");
  }

  if (intent === "thanks") {
    return addMessage(lang === "ar" ? "🌟 العفو! سعيد بخدمتك." : "🌟 You're welcome! Happy to assist you.", "bot");
  }

  if (intent === "contact") {
    return addMessage(lang === "ar" ? "📞 يمكنك التواصل معنا عبر الرقم 123456789 أو عبر البريد support@example.com." : "📞 Contact us at 123456789 or via email support@example.com.", "bot");
  }

  if (intent === "location") {
    return addMessage(lang === "ar" ? "📍 موقعنا: جامعة الإمام عبدالرحمن بن فيصل، الدمام." : "📍 Our location: Riyadh, Saudi Arabia.", "bot");
  }

  if (intent === "working_hours") {
    return addMessage(lang === "ar" ? "🕒 أوقات العمل: الأحد إلى الخميس، 9 صباحاً حتى 5 مساءً." : "🕒 Working hours: Sunday to Thursday, 9 AM to 5 PM.", "bot");
  }

  if (intent === "logout") {
    return addMessage(lang === "ar" ? "🔒 لتسجيل الخروج، اضغط على زر تسجيل الخروج بحسابك." : "🔒 To logout, click the logout button in your account.", "bot");
  }

  if (intent === "who_are_you") {
    return addMessage(lang === "ar" ? "🤖 أنا بوت خدمة المفقودات هنا لمساعدتك." : "🤖 I'm the Lost & Found Service Bot here to assist you.", "bot");
  }

  if (intent === "report_status") {
    return addMessage(lang === "ar" ? "📝 يمكنك متابعة حالة بلاغك من خلال قسم (بحث بلاغ) بحسابك." : "📝 You can check your report status through the (Search Report) section in your account.", "bot");
  }

  if (intent === "greeting") {
    return addMessage(lang === "ar" ? "👋 أهلًا وسهلًا بك! كيف أقدر أساعدك اليوم؟" : "👋 Hello! How can I assist you today?", "bot");
  }

  if (intent === "how_are_you") {
    return addMessage(lang === "ar" ? "😊 أنا بخير، شكراً لسؤالك! وأنت كيف حالك؟" : "😊 I'm good, thanks for asking! How about you?", "bot");
  }

  addMessage(lang === "ar" ? "❓ لم أفهم تمامًا... ممكن توضح أكثر؟" : "❓ I didn't quite understand... Could you please clarify?", "bot");
}

function newChat() {
  document.getElementById("chatInner").innerHTML = "";
  const lang = getLang();
  setTimeout(() => {
    addMessage(lang === "ar" ? "👋 مرحبًا بك! كيف يمكنني مساعدتك اليوم؟" : "👋 Welcome! How can I assist you today?", "bot");
  }, 300);
}
