import os
import json
from itertools import chain
import cherrypy
from giddle.models import Question, PlayedQuestion
from giddle.controllers import AnswerEvaluator

PATH = os.path.abspath(os.path.dirname(__file__))
class Root(object):
    pass


class WebApp(object):
    max_errors = 4
    n_answers = 6
    n_consecutive_wrong_answers_before_hint = 2

    def _response(self, response, additional_info={}):
        session_info = {
            'sid' : cherrypy.session.id,
            'ip'  : cherrypy.request.remote.ip
        }
        dict_to_log = dict(additional_info.items()
                                +response.items()+session_info.items())
        cherrypy.log(json.dumps(dict_to_log))
        return response

    def _initialise_score(self, reset=False):
        if 'score' not in cherrypy.session:
            cherrypy.session['score'] = 0
        if reset or 'consecutive_errors' not in cherrypy.session:
           cherrypy.session['consecutive_errors'] = 0
        if reset or 'errors' not in cherrypy.session:
           cherrypy.session['errors'] = 0
        if reset:
            cherrypy.session['played_question'] = None

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_question(self):
        self._initialise_score(reset=True)
        question = Question.get_random()
        cherrypy.session['played_question'] = PlayedQuestion(question)
        return self._response({
            'question': question.query,
            'score'   : cherrypy.session['score']
        })

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def evaluate_answer(self, proposal):
        self._initialise_score(reset=False)
        played_question = cherrypy.session.get('played_question')
        if not played_question:
            raise cherrypy.HTTPError(400, "No question found.")
        answer_result = AnswerEvaluator().evaluate(played_question, proposal)

        # Update counts
        if answer_result:
            cherrypy.session['score'] += 1
            cherrypy.session['consecutive_errors'] = 0
            played_question.add_answer_found(answer_result)
        else:
            cherrypy.session['consecutive_errors'] += 1
            cherrypy.session['errors'] += 1

        # Determine status
        if len(played_question.answers_found) >= self.n_answers:
            status = 'won'
            self._initialise_score(reset=True)
        elif cherrypy.session['errors'] >= self.max_errors:
            status = 'lost'
            self._initialise_score(reset=True)
        else:
            status = 'guessing'

        # Build response
        response = {}
        response['status'] = status
        response['correct'] = bool(answer_result)
        response['score'] = cherrypy.session['score']
        response['hint'] = played_question.hint \
            if cherrypy.session['consecutive_errors'] >= self.n_consecutive_wrong_answers_before_hint \
            else ''
        response['answers'] = [[str(a), True] for a in played_question.answers_found]
        if status == 'lost':
            response['answers'] += [[str(a), False] for a in played_question.remaining_meta_answers]

        return response


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on'     : True,
            'tools.sessions.timeout': 10080,
            'tools.staticdir.on'    : True,
            'tools.staticdir.dir'   : os.path.join(PATH, 'static'),
            'tools.staticdir.index' : 'index.html'
        }
    }
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', '8080')),
        'cherrypy.log.error_log.propagate' : False,
        'cherrypy.log.access_log.propagate' : False,
    })
    cherrypy.quickstart(WebApp(), '/', conf)