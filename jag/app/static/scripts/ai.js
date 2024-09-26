
// Perform OCR locally
function doOcr() {
    var formData = new FormData(document.getElementById('ocrForm'));
    $.ajax({
        url: '/do-ocr',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            $('#ocrText').text(data.extracted_text);
             if (window.autoContinue) submitOcr();
        },
        error: function () {
            alert('Failed to process image.');
        }
    });
}

// Submits OCR text to Chat GPT for further refinement
function submitOcr() {
    let formData = new FormData(document.getElementById('submit-ocr-text-form'));
    let question_text = $('#ocrText').text();
    formData.append('question_text', question_text);
    let topics = $('#topics-input-form-field').val();
    formData.append('topics', topics);

    $.ajax({
        url: '/submit-ocr',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            let formattedQuestion = data.cleaned_question.replace(/\n/g, '<br>');
            // let formattedAnswer = data.answer_section.replace(/\n/g, '<br>');

            document.getElementById('extracted_question').textContent = formattedQuestion;
            // document.getElementById('extracted_a_section').textContent =
            // formattedAnswer;
            if (window.autoContinue) getAnswer();
        },
        error: function () {
            alert('Failed to get an answer.');
        }
    });
}

// OpenAI/ ChatGPT Only (send the Cleaned OCR Result to GPT)
function getAnswer() {
    let formData = new FormData(document.getElementById('get-answer'));

    let extracted_question = $('#extracted_question').text();
    formData.append('extracted_question', extracted_question);
    // formData.append('extracted_answer_section', $('#extracted_answer_section').text());

    $.ajax({
        url: '/get-answer',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            document.getElementById('ai_answer').textContent = data.ai_answer;
            window.autoContinue = false;
        },
        error: function () {
            alert('Failed to get an answer.');
        }
    });
}

function doAllSteps() {
    window.autoContinue = true;
    doOcr();
}

