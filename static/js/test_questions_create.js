const CSRF_TOKEN = document.getElementById('csrf_token').value
const QUESTION_REGEX = /(?<=questions\-)(\d+)(?=\-)/
const ANSWER_REGEX = /(?<=questions\-\d+\-answers-)(\d+)(?=\-)/
const POINT_CATEGORIES_OPTIONS_HTML = $(document).find('[name="questions-0-answers-0-negative_point_category_id"]')[0].innerHTML

// TODO: Repair regex replacing, add questions adding, removing and changing order
const insertAnswer = (event) => {
    let questionElement = $(event.target).closest('.question')
    let questionIndex = $($(questionElement).find('[name]')[0]).attr('name').match(QUESTION_REGEX)[1]
    let answerIndex = $(questionElement).find('.answer').length
    
    let answerElement = getAnswerTemplate(questionIndex, answerIndex)
    
    $(questionElement).find('.answers').append(answerElement)
}

const insertQuestion = (event) => {
    let questionIndex = document.querySelectorAll('.question')['length']
    let element = `<div class="question card border border-dark">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="d-inline-block">Question</h5>
            <span>
                <button type="button" class="move-up-question btn btn-mini btn-primary ml-auto" onclick="moveUpQuestion(event)">Move up</button>
                <button type="button" class="move-down-question btn btn-mini btn-primary ml-4" onclick="moveDownQuestion(event)">Move down</button>
                <button type="button" class="delete-question btn btn-mini btn-danger ml-4" onclick="deleteClosestQuestion(event)">Delete</button>
            </span>
        </div>
        <div class="card-body">
            <input name="questions-${questionIndex}-id" type="hidden" value="${crypto.randomUUID()}">
            <input name="questions-${questionIndex}-csrf_token" type="hidden" value="${CSRF_TOKEN}">
            <label class="form-group w-100 mb-3">
                <span class="d-block">Content</span>
                <input class="form-control" maxlength="255" minlength="1" name="questions-${questionIndex}-content" required type="text" value="">
            </label>
            <label class="form-group w-100 mb-3">
                <span class="d-block">Answer Type</span>
                <select class="form-control" name="questions-${questionIndex}-answer_type" required>
                    <option value="slider">Slider</option>
                    <option value="single_choice">Single Choice</option>
                    <option value="multiple_choice">Multiple Choice</option>
                </select>
            </label>
            <h4 class="mt-4">Answers</h4>
            <div class="answers mb-3">${getAnswerTemplate(questionIndex, 0)}</div>
            <button type="button" class="btn btn-primary w-100" onclick="insertAnswer(event)">Add new answer</button>
        </div>
    </div>`
    
    $('.questions').append(element)
}

const getAnswerTemplate = (questionIndex, answerIndex) => `<div class="answer card border border-dark">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="d-inline-block">Answer</h5>
            <span>
                <button type="button" class="move-up-answer btn btn-mini btn-primary ml-auto" onclick="moveUpAnswer(event)">Move up</button>
                <button type="button" class="move-down-answer btn btn-mini btn-primary ml-4" onclick="moveDownAnswer(event)">Move down</button>
                <button type="button" class="delete-answer btn btn-mini btn-danger ml-4" onclick="deleteClosestAnswer(event)">Delete</button>
            </span>
        </div>
        <div class="card-body">
            <input type="hidden" name="questions-${questionIndex}-answers-${answerIndex}-id" value="${crypto.randomUUID()}">
            <input type="hidden" name="questions-${questionIndex}-answers-${answerIndex}-csrf_token" value="${CSRF_TOKEN}">
            <label class="form-group w-100 mb-3">
                <span class="d-block">Content</span>
                <input type="text" name="questions-${questionIndex}-answers-${answerIndex}-content" class="form-control mb-3" minlength="1" maxlength="255" required>
            </label>
            <label class="form-group w-100 mb-3">
                <span class="d-block">Points if not selected (or left on slide)</span>
                <input type="number" name="questions-${questionIndex}-answers-${answerIndex}-min_points" class="form-control mb-3" value="0" required>
            </label>
            <label class="form-group w-100 mb-3">
                <span class="d-block">Points if selected (or right on slide)</span>
                <input type="number" name="questions-${questionIndex}-answers-${answerIndex}-max_points" class="form-control mb-3" value="0" required>
            </label>
            <label class="form-group w-100 mb-3">
                <span class="d-block">Point step on slider</span>
                <input type="number" name="questions-${questionIndex}-answers-${answerIndex}-step" class="form-control mb-3" min="1" value="1">
            </label>
            <label class="form-group w-100 mb-3">
                <span class="d-block">First label (required, on slider on left)</span>
                <input type="text" name="questions-${questionIndex}-answers-${answerIndex}-first_label" class="form-control mb-3" minlength="1" maxlength="255" required>
            </label>
            <label class="form-group w-100 mb-3">
                <span class="d-block">Second label (only on slider on right)</span>
                <input type="text" name="questions-${questionIndex}-answers-${answerIndex}-second_label" class="form-control mb-3" minlength="1" maxlength="255">
            </label>
            <label class="form-group w-100 mb-3">
                <span class="d-block">Point category (left on slider)</span>
                <select class="form-control" name="questions-${questionIndex}-answers-${answerIndex}-negative_point_category_id" required>
                    ${POINT_CATEGORIES_OPTIONS_HTML}
                </select>
            </label>
            <label class="form-group w-100 mb-3">
                <span class="d-block">Right slider point category</span>
                <select class="form-control" name="questions-${questionIndex}-answers-${answerIndex}-positive_point_category_id" required>
                    ${POINT_CATEGORIES_OPTIONS_HTML}
                </select>
            </label>
        </div>
    </div>`

const debug = () => {
    let questions = $('.question')
    let result = []
    for (i = 0; i < questions.length; i++) {
        result.push($(questions[i]).find('input').attr('name'))
        answers = $(questions[i]).find('.answers').children()
        for (j = 0; j < answers.length; j++) {
            result.push($(answers[j]).find('input').attr('name'))
        }
    }
    return result
}

const moveDownAnswer = moveDown('.answer', ANSWER_REGEX)
const moveUpAnswer = moveUp('.answer', ANSWER_REGEX)
const deleteClosestAnswer = deleteClosest('.answer', ANSWER_REGEX)
const moveDownQuestion = moveDown('.question', QUESTION_REGEX)
const moveUpQuestion = moveUp('.question', QUESTION_REGEX)
const deleteClosestQuestion = deleteClosest('.question', QUESTION_REGEX)