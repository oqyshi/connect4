from django.shortcuts import render, redirect
from django.views import View

from .game_logic import (
	new_board,
	check_winner,
	apply_move,
	ROWS,
	COLS,
	PLAYERS,
	AVAILABLE_TOKENS,
	TOKEN_COLORS,
)

MIN_ROWS, MAX_ROWS = 4, 12
MIN_COLS, MAX_COLS = 4, 15


class GameView(View):
	template_name = 'game/index.html'

	def _ensure_session(self, session):
		if 'board' not in session:
			rows = session.get('rows', ROWS)
			cols = session.get('cols', COLS)
			session['board'] = new_board(rows, cols)
			session['players'] = PLAYERS
			session['turn'] = session['players'][0]
			session['winner'] = None

	def get(self, request):
		session = request.session
		self._ensure_session(session)

		rows = session.get('rows', ROWS)
		cols = session.get('cols', COLS)
		turn = session.get('turn', session.get('players', PLAYERS)[0])
		winner = session.get('winner')
		context = {
			'board': session.get('board'),
			'turn': turn,
			'players': session.get('players', PLAYERS),
			'winner': winner,
			'rows_range': range(rows),
			'cols_range': range(cols),
			'available_tokens': AVAILABLE_TOKENS,
			'player_counts': list(range(2, len(AVAILABLE_TOKENS) + 1)),
			'token_colors': TOKEN_COLORS,
			'message': session.pop('message', None),
			'turn_color': TOKEN_COLORS.get(turn, '#cccccc'),
			'winner_color': TOKEN_COLORS.get(winner, '#cccccc'),
			'rows': rows,
			'cols': cols,
			'min_rows': MIN_ROWS,
			'max_rows': MAX_ROWS,
			'min_cols': MIN_COLS,
			'max_cols': MAX_COLS,
		}
		return render(request, self.template_name, context)

	def post(self, request):
		session = request.session
		self._ensure_session(session)

		action = request.POST.get('action')
		if action == 'restart':
			rows = session.get('rows', ROWS)
			cols = session.get('cols', COLS)
			session['board'] = new_board(rows, cols)
			session['players'] = session.get('players', PLAYERS)
			session['turn'] = session['players'][0]
			session['winner'] = None
			return redirect('game:index')

		if action == 'set_size':
			try:
				rows = int(request.POST.get('rows'))
				cols = int(request.POST.get('cols'))
			except (TypeError, ValueError):
				return redirect('game:index')
			rows = max(MIN_ROWS, min(MAX_ROWS, rows))
			cols = max(MIN_COLS, min(MAX_COLS, cols))
			session['rows'] = rows
			session['cols'] = cols
			session['board'] = new_board(rows, cols)
			session['players'] = session.get('players', PLAYERS)
			session['turn'] = session['players'][0]
			session['winner'] = None
			return redirect('game:index')

		if action == 'set_players':
			n = request.POST.get('num_players')
			try:
				n = int(n)
			except (TypeError, ValueError):
				return redirect('game:index')
			min_p = 2
			max_p = len(AVAILABLE_TOKENS)
			if n < min_p or n > max_p:
				return redirect('game:index')

			rows = session.get('rows', ROWS)
			cols = session.get('cols', COLS)
			session['players'] = AVAILABLE_TOKENS[:n]
			session['board'] = new_board(rows, cols)
			session['turn'] = session['players'][0]
			session['winner'] = None
			return redirect('game:index')

		winner = session.get('winner')
		if winner:
			return redirect('game:index')

		col = request.POST.get('col')
		try:
			col = int(col)
		except (TypeError, ValueError):
			return redirect('game:index')

		cols = session.get('cols', COLS)
		turn = session.get('turn', session.get('players', PLAYERS)[0])
		if 0 <= col < cols:
			placed, board, win, next_turn = apply_move(
				session.get('board'), col, turn, players=session.get('players', PLAYERS)
			)
			if not placed:
				session['message'] = 'Column is full'
				return redirect('game:index')
			if placed:
				if win:
					session['winner'] = win
				else:
					session['turn'] = next_turn
				session['board'] = board

		return redirect('game:index')
