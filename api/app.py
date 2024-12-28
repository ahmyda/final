from flask import Flask, render_template, request ,session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session


# Sample quiz data (you can replace this with a full set of 50 questions)
data = [
 {'question': 'What does a Conversational Implicature depend on?', 'options': ['The truth of the statement', 'Contextual assumptions', 'The speaker’s attitude', 'Grammatical rules'], 'answer': 'Contextual assumptions'},
{'question': 'What is the key feature of a Directive Speech Act?', 'options': ['Requesting action from the listener', 'Describing a state of the world', 'Expressing feelings', 'Changing the world through utterances'], 'answer': 'Requesting action from the listener'},
{'question': 'What is an example of a Speech Act that expresses emotions?', 'options': ['Apology', 'Promise', 'Request', 'Order'], 'answer': 'Apology'},
{'question': 'What is the key function of a Declarative Speech Act?', 'options': ['Making a statement or assertion', 'Requesting action', 'Expressing a feeling', 'Giving a command'], 'answer': 'Making a statement or assertion'},
{'question': 'Which maxim requires speakers to avoid unnecessary information?', 'options': ['Maxim of Quantity', 'Maxim of Quality', 'Maxim of Manner', 'Maxim of Relation'], 'answer': 'Maxim of Quantity'},
{'question': 'What is the purpose of Grice’s Maxim of Manner?', 'options': ['Avoid vagueness and ambiguity', 'Provide sufficient information', 'Be truthful', 'Maintain relevance'], 'answer': 'Avoid vagueness and ambiguity'},
{'question': 'Which type of Speech Act includes an apology?', 'options': ['Commissive', 'Expressive', 'Representative', 'Directive'], 'answer': 'Expressive'},
{'question': 'Which presupposition type is linked with "whether" clauses?', 'options': ['Existential', 'Factive', 'Structural', 'Counterfactual'], 'answer': 'Counterfactual'},
{'question': 'What is an example of a Conventional Implicature?', 'options': ['"John is a bachelor, so he is unmarried."', '"He said he was sorry."', '"I think he is coming."', '"It’s raining, but I like it."'], 'answer': '"John is a bachelor, so he is unmarried."'},
{'question': 'What kind of Presupposition is typically triggered by negation?', 'options': ['Factive', 'Existential', 'Counterfactual', 'Structural'], 'answer': 'Existential'},
{'question': 'Which of the following is a Commissive Speech Act?', 'options': ['Promise', 'Order', 'Suggestion', 'Command'], 'answer': 'Promise'},
{'question': 'What is the Maxim of Quality focused on?', 'options': ['Providing the most detailed information', 'Being relevant to the topic', 'Being truthful', 'Avoiding redundancy'], 'answer': 'Being truthful'},
{'question': 'Which type of Speech Act is focused on making requests?', 'options': ['Directive', 'Commissive', 'Expressive', 'Representative'], 'answer': 'Directive'},
{'question': 'What does a Declarative Speech Act do?', 'options': ['Asserts a fact', 'Requests action', 'Expresses an emotion', 'Makes a promise'], 'answer': 'Asserts a fact'},
{'question': 'What kind of Speech Act is "I promise to help you"?', 'options': ['Commissive', 'Directive', 'Representative', 'Expressive'], 'answer': 'Commissive'},
{'question': 'Which presupposition type is most commonly associated with definite noun phrases?', 'options': ['Existential', 'Factive', 'Counterfactual', 'Structural'], 'answer': 'Existential'},
{'question': 'In Grice’s theory, what is the function of the Maxim of Relation?', 'options': ['To be relevant in communication', 'To avoid contradictions', 'To provide sufficient information', 'To be concise'], 'answer': 'To be relevant in communication'},
{'question': 'Which type of Speech Act is "I apologize for being late"?', 'options': ['Commissive', 'Expressive', 'Directive', 'Representative'], 'answer': 'Expressive'},
{'question': 'What does the Maxim of Quantity require?', 'options': ['To avoid over-explaining', 'To provide enough information', 'To be concise and clear', 'To be truthful'], 'answer': 'To provide enough information'},
{'question': 'What does an Implicature depend on?', 'options': ['The literal meaning of words', 'The listener’s understanding of the context', 'The syntactic structure of the sentence', 'The tone of voice'], 'answer': 'The listener’s understanding of the context'},
{'question': 'Which of the following is an example of a Representative Speech Act?', 'options': ['Stating a fact', 'Asking a question', 'Making a promise', 'Giving a command'], 'answer': 'Stating a fact'},
{'question': 'What is the main role of Deixis in communication?', 'options': ['To refer to objects and times in relation to the speaker and listener', 'To create metaphors', 'To add complexity to syntax', 'To imply truthfulness'], 'answer': 'To refer to objects and times in relation to the speaker and listener'},
{'question': 'What is a "factive" presupposition?', 'options': ['Assumes the truth of a proposition', 'Assumes that something is possible', 'Assumes something false', 'Assumes an action will happen'], 'answer': 'Assumes the truth of a proposition'},
{'question': 'Which maxim is broken when a speaker gives irrelevant information?', 'options': ['Maxim of Manner', 'Maxim of Relation', 'Maxim of Quality', 'Maxim of Quantity'], 'answer': 'Maxim of Relation'},
{'question': 'What is the function of Grice’s Maxim of Quality?', 'options': ['To be truthful', 'To be clear', 'To avoid vagueness', 'To be concise'], 'answer': 'To be truthful'},
{'question': 'What is an example of a Counterfactual Presupposition?', 'options': ['"If I were rich, I would travel."', '"She has been studying all day."', '"He apologized for the mistake."', '"The door is locked."'], 'answer': '"If I were rich, I would travel."'},
{'question': 'Which maxim is violated when a speaker tells a lie?', 'options': ['Maxim of Quantity', 'Maxim of Quality', 'Maxim of Manner', 'Maxim of Relation'], 'answer': 'Maxim of Quality'},
{'question': 'What does an illocutionary act express?', 'options': ['The speaker’s intent in making the utterance', 'The context in which the utterance occurs', 'The grammatical structure of the sentence', 'The listener’s interpretation'], 'answer': 'The speaker’s intent in making the utterance'},
{'question': 'What is the difference between presupposition and implicature?', 'options': ['Presupposition is context-dependent, implicature is not', 'Presupposition remains even if the sentence is negated, implicature does not', 'Implicature is more directly connected to syntax', 'There is no difference between them'], 'answer': 'Presupposition remains even if the sentence is negated, implicature does not'},
{'question': 'Which category of Speech Act involves making statements that assert facts or opinions?', 'options': ['Representatives', 'Directives', 'Commissives', 'Expressives'], 'answer': 'Representatives'},
{'question': 'In Pragmatics, what does "context" refer to?', 'options': ['The syntactic structure of language', 'The social and physical environment of communication', 'The grammar of a language', 'The sound of words'], 'answer': 'The social and physical environment of communication'},
{'question': 'What type of presupposition is often triggered by the verb "stop"?', 'options': ['Factive', 'Existential', 'Counterfactual', 'Structural'], 'answer': 'Existential'},
{'question': 'Which of these is an example of an indirect request?', 'options': ['"Can you close the window?"', '"Close the window."', '"I need you to close the window."', '"The window is closed."'], 'answer': '"Can you close the window?"'},
{'question': 'What is the purpose of Grice’s Maxim of Manner?', 'options': ['To ensure the speaker is truthful', 'To avoid ambiguity and vagueness', 'To provide enough information', 'To make the conversation relevant'], 'answer': 'To avoid ambiguity and vagueness'},
{'question': 'What does the term "implicature" refer to in Pragmatics?', 'options': ['Information inferred from context', 'The literal meaning of words', 'The grammatical structure of a sentence', 'The truth of the statement'], 'answer': 'Information inferred from context'},
{'question': 'What does a "direct speech act" involve?', 'options': ['A speaker’s intention and the listener’s interpretation match', 'The listener interprets the act indirectly', 'The speaker uses figurative language', 'The speaker expresses feelings'], 'answer': 'A speaker’s intention and the listener’s interpretation match'},
{'question': 'What type of Speech Act includes making a promise?', 'options': ['Commissive', 'Directive', 'Expressive', 'Representative'], 'answer': 'Commissive'},
{'question': 'What is the role of Speech Act Theory?', 'options': ['To analyze sentence structure', 'To study the meaning behind words', 'To explore how language functions in communication', 'To analyze the grammar of sentences'], 'answer': 'To explore how language functions in communication'},
{'question': 'Which category of Speech Acts changes the world through the act of speaking?', 'options': ['Representatives', 'Directives', 'Declarations', 'Expressives'], 'answer': 'Declarations'},
{'question': 'Which presupposition type is triggered by the verb "forget"?', 'options': ['Factive', 'Existential', 'Counterfactual', 'Structural'], 'answer': 'Factive'},
{'question': 'What is an example of a Structural Presupposition?', 'options': ['"The king of France is bald."', '"He stopped smoking."', '"I didn’t know he was here."', '"We were waiting for the bus."'], 'answer': '"The king of France is bald."'},
{'question': 'What is the Maxim of Quality concerned with?', 'options': ['Providing enough information', 'Avoiding ambiguity', 'Being truthful', 'Being concise'], 'answer': 'Being truthful'},
{'question': 'What kind of Speech Act expresses the speaker’s psychological state?', 'options': ['Commissive', 'Directive', 'Expressive', 'Representative'], 'answer': 'Expressive'},
{'question': 'Which of the following is an example of a Directive Speech Act?', 'options': ['"Please help me."', '"I promise to help."', '"I apologize for being late."', '"The sky is blue."'], 'answer': '"Please help me."'},
{'question': 'What is an example of a Representative Speech Act?', 'options': ['"I believe it will rain tomorrow."', '"Could you pass me the salt?"', '"I apologize for the mistake."', '"I suggest we take a break."'], 'answer': '"I believe it will rain tomorrow."'},
{'question': 'Which of the following would violate the Maxim of Relation?', 'options': ['Giving irrelevant information', 'Providing insufficient details', 'Being too vague', 'Using incorrect grammar'], 'answer': 'Giving irrelevant information'},
{'question': 'What is the purpose of an Illocutionary Act?', 'options': ['To express feelings', 'To perform actions through utterances', 'To make requests', 'To give commands'], 'answer': 'To perform actions through utterances'},
{'question': 'What does a "factive" verb do?', 'options': ['Presupposes the truth of its complement', 'Requires a question to be asked', 'States a fact', 'Makes a suggestion'], 'answer': 'Presupposes the truth of its complement'},
{'question': 'What does the Maxim of Manner advise?', 'options': ['To be clear and avoid ambiguity', 'To avoid exaggeration', 'To be relevant', 'To speak truthfully'], 'answer': 'To be clear and avoid ambiguity'},
{'question': 'What is Pragmatics primarily concerned with?', 'options': ['The structure of sentences', 'The study of meaning in context', 'The phonetics of language', 'The syntax of communication'], 'answer': 'The study of meaning in context'},
{'question': 'According to Pragmatics, what influences how much speakers need to say?', 'options': ['Grammar rules', 'Proximity of the listener', 'Dictionary definitions', 'Writing style'], 'answer': 'Proximity of the listener'},
{'question': 'What are Speech Acts?', 'options': ['Actions performed through utterances', 'Rules for sentence formation', 'Methods of pronunciation', 'Types of formal speeches'], 'answer': 'Actions performed through utterances'},
{'question': 'What is an Illocutionary Act?', 'options': ['The literal meaning of words', 'The intended function of an utterance', 'The effect on the listener', 'The syntactic structure of a sentence'], 'answer': 'The intended function of an utterance'},
{'question': 'Which category does a promise belong to in Searle’s classification of Speech Acts?', 'options': ['Representative', 'Directive', 'Commissive', 'Expressive'], 'answer': 'Commissive'},
{'question': 'What is the function of Representatives in Speech Acts?', 'options': ['Commit the speaker to an action', 'Change the state of the world', 'Commit the speaker to the truth of a proposition', 'Express emotions or attitudes'], 'answer': 'Commit the speaker to the truth of a proposition'},
{'question': 'What do Felicity Conditions ensure?', 'options': ['Proper grammar usage', 'Successful performance of Speech Acts', 'Clarity of speech', 'Proper intonation'], 'answer': 'Successful performance of Speech Acts'},
{'question': 'What type of presupposition assumes information within a definite noun phrase?', 'options': ['Factive', 'Structural', 'Existential', 'Counterfactual'], 'answer': 'Existential'},
{'question': 'In Grice’s Maxims, which principle relates to truthfulness?', 'options': ['Quantity', 'Quality', 'Relation', 'Manner'], 'answer': 'Quality'},
{'question': 'What is a Conventional Implicature?', 'options': ['Context-specific meaning', 'Meaning derived from word choice', 'Meaning inferred from actions', 'Meaning dependent on listener’s perception'], 'answer': 'Meaning derived from word choice'},
{'question': 'What is an example of an Existential Presupposition?', 'options': ['"She stopped smoking."', '"His book is on the table."', '"I dreamed I was flying."', '"Where did you go?"'], 'answer': '"His book is on the table."'},
{'question': 'According to Grice, how can maxims be violated?', 'options': ['By following grammar strictly', 'Through deliberate exaggeration', 'By adhering to relevance', 'Through clarity in speech'], 'answer': 'Through deliberate exaggeration'},
{'question': 'What is the Maxim of Relation?', 'options': ['Be truthful', 'Be relevant', 'Avoid ambiguity', 'Provide sufficient information'], 'answer': 'Be relevant'},
{'question': 'What is a Perlocutionary Force?', 'options': ['The literal content of a sentence', 'The intended function of an utterance', 'The effect achieved on the listener', 'The grammatical structure'], 'answer': 'The effect achieved on the listener'},
{'question': 'What is the Cooperative Principle?', 'options': ['Making contributions relevant to context', 'Following grammatical norms', 'Using complex structures for clarity', 'Providing literal meanings'], 'answer': 'Making contributions relevant to context'},
{'question': 'What is the key feature of Structural Presuppositions?', 'options': ['Information assumed within sentence structure', 'Assumptions about the listener’s beliefs', 'Truth derived from propositions', 'Conditions for felicity'], 'answer': 'Information assumed within sentence structure'},
{'question': 'Which category includes “I apologize”?', 'options': ['Commissives', 'Directives', 'Expressives', 'Declarations'], 'answer': 'Expressives'},
{'question': 'What is the Maxim of Quantity?', 'options': ['Provide sufficient information', 'Be truthful', 'Be clear', 'Be relevant'], 'answer': 'Provide sufficient information'},
{'question': 'What is an example of a Directive?', 'options': ['"I name this ship Freedom."', '"Please pass the salt."', '"The Earth is round."', '"I promise to help you."'], 'answer': '"Please pass the salt."'},
{'question': 'What is a Hedge?', 'options': ['A cautious way to avoid being categorical', 'A direct command', 'A type of indirect speech act', 'A way to assert authority'], 'answer': 'A cautious way to avoid being categorical'},
{'question': 'Which maxim is broken in the statement: "It starts at 3 PM sharp." when the event was delayed?', 'options': ['Relation', 'Quality', 'Manner', 'Quantity'], 'answer': 'Quality'},
{'question': 'What does “context” refer to in Pragmatics?', 'options': ['The background knowledge relevant to an utterance', 'The phonetics of a sentence', 'The syntactic structure', 'Grammatical norms'], 'answer': 'The background knowledge relevant to an utterance'},
{'question': 'What kind of Deixis relates to time?', 'options': ['Personal', 'Spatial', 'Temporal', 'Referential'], 'answer': 'Temporal'},
{'question': 'What is the main feature of a Counterfactual Presupposition?', 'options': ['It assumes the truth of a fact', 'It assumes something false', 'It relies on context for meaning', 'It asserts future actions'], 'answer': 'It assumes something false'},
{'question': 'In the sentence, "He stopped running," what is presupposed?', 'options': ['He was running previously', 'He will run again', 'He never ran', 'Running is not possible'], 'answer': 'He was running previously'},
{'question': 'What is an example of an Indirect Speech Act?', 'options': ['"Can you close the door?" (intended as a request)', '"Close the door."', '"I am asking you to close the door."', '"The door is closed."'], 'answer': '"Can you close the door?" (intended as a request)'},
{'question': 'What is a Declarative Speech Act?', 'options': ['Describing the state of the world', 'Changing the world through an utterance', 'Asking a question', 'Expressing an opinion'], 'answer': 'Changing the world through an utterance'},
{'question': 'What is the role of Perlocutionary Forces?', 'options': ['Achieving an effect on the listener', 'Expressing grammatical forms', 'Stating facts', 'Creating propositions'], 'answer': 'Achieving an effect on the listener'},
{'question': 'What is Entailment?', 'options': ['What logically follows from an utterance', 'A speaker’s assumptions', 'A grammatical rule', 'A metaphorical meaning'], 'answer': 'What logically follows from an utterance'},
{'question': 'In "What a great performance!" what kind of Speech Act is this?', 'options': ['Directive', 'Expressive', 'Commissive', 'Declarative'], 'answer': 'Expressive'},
{'question': 'What kind of implicature arises irrespective of context?', 'options': ['Conventional', 'Particularized Conversational', 'Generalized Conversational', 'Structural'], 'answer': 'Conventional'},
{'question': 'In the utterance, "Oh, by the way, I met your friend," what linguistic feature is present?', 'options': ['Hedge', 'Directive', 'Expressive', 'Implicature'], 'answer': 'Hedge'},
{'question': 'How does Pragmatics differ from Semantics?', 'options': ['It studies sentence structure', 'It focuses on meaning in context', 'It decodes literal meanings', 'It follows syntactic rules'], 'answer': 'It focuses on meaning in context'},
{'question': 'In "I now pronounce you husband and wife," what Speech Act is performed?', 'options': ['Directive', 'Declaration', 'Expressive', 'Commissive'], 'answer': 'Declaration'},
{'question': 'What does the Maxim of Manner suggest?', 'options': ['Avoid ambiguity', 'Provide sufficient details', 'Be truthful', 'Be relevant'], 'answer': 'Avoid ambiguity'},
{'question': 'What is the function of an Expressive?', 'options': ['Commit to future action', 'State the truth of a proposition', 'Indicate psychological states', 'Change the world'], 'answer': 'Indicate psychological states'},
{'question': 'What does a Factive Presupposition rely on?', 'options': ['Non-truths', 'Context-specific information', 'Assumed facts', 'Syntactic structures'], 'answer': 'Assumed facts'},
{'question': 'What is the effect of violating the Maxim of Quality?', 'options': ['Irrelevance in communication', 'Lack of truthfulness', 'Over-information', 'Ambiguity'], 'answer': 'Lack of truthfulness'},
{'question': 'What kind of Deixis is present in "Bring it back tomorrow"?', 'options': ['Temporal', 'Spatial', 'Personal', 'Referential'], 'answer': 'Temporal'},
{'question': 'What is the main idea of the Cooperative Principle?', 'options': ['Speaking grammatically', 'Being concise', 'Contributing relevant and clear information', 'Maintaining politeness'], 'answer': 'Contributing relevant and clear information'},
{'question': 'Which of the following is a Commissive Speech Act?', 'options': ['Promise', 'Order', 'Apology', 'Question'], 'answer': 'Promise'},
{'question': 'What does the Maxim of Quantity require?', 'options': ['Give enough information', 'Be truthful', 'Be relevant', 'Be clear'], 'answer': 'Give enough information'},
{'question': 'What is the function of a Representative?', 'options': ['Commit to the truth of a proposition', 'Request action', 'Express emotion', 'Change the world'], 'answer': 'Commit to the truth of a proposition'},
{'question': 'Which category of Speech Acts focuses on actions through words?', 'options': ['Commissive', 'Directive', 'Expressive', 'Representative'], 'answer': 'Commissive'},
{'question': 'In Grice’s Maxims, what does the Maxim of Quality ensure?', 'options': ['Clarity of speech', 'Truthfulness', 'Proper volume', 'Relevant details'], 'answer': 'Truthfulness'},
{'question': 'What is the main purpose of Speech Act Theory?', 'options': ['To study the structure of sentences', 'To understand the social function of language', 'To analyze word meanings', 'To define grammatical rules'], 'answer': 'To understand the social function of language'},
{'question': 'Which of the following is an example of a Factive Presupposition?', 'options': ['"She forgot to call."', '"He stopped playing."', '"I didn’t know he was there."', '"They are coming tomorrow."'], 'answer': '"She forgot to call."'},
{'question': 'What does the term "indirect speech act" refer to?', 'options': ['Speech acts that require context to be understood', 'The literal meaning of a sentence', 'Actions performed directly through speech', 'Speech acts that imply more than they directly express'], 'answer': 'Speech acts that imply more than they directly express'},
{'question': 'What is the role of Grice’s Maxim of Quality?', 'options': ['To avoid exaggeration', 'To provide enough information', 'To avoid ambiguity', 'To provide truthful information'], 'answer': 'To provide truthful information'}
]


@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)


@app.route('/')
def index():
    # Randomly select 10 questions
    selected_questions = random.sample(data, 10)
    for question in selected_questions:
        random.shuffle(question['options'])
    session['selected_questions'] = selected_questions  # Store the selected questions in the session
    return render_template('index.html', questions=selected_questions)


@app.route('/result', methods=['POST'])
def result():
    score = 0
    selected_questions = session.get('selected_questions', [])  # Retrieve the selected questions from the session
    user_answers = []  # To store user's answers
    correct_answers = []  # To store correct answers

    for i, question in enumerate(selected_questions):
        user_answer = request.form.get(f'question-{i}')
        user_answers.append(user_answer)  # Store user's answer
        correct_answers.append(question['answer'])  # Store correct answer
        if user_answer == question['answer']:
            score += 1

    return render_template('result.html', score=score, total=10, user_answers=user_answers, correct_answers=correct_answers, questions=selected_questions)





if __name__ == '__main__':
    app.run(debug=True)
