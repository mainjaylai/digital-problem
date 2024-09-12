import copy
import json
from queue import Queue

from django.http import HttpResponse
from django.shortcuts import render
from .soluton import Solve
from .grid import Grid

target = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


def Push(solve):
    res = {}
    res["time"] = solve.run_time
    res["memory"] = solve.memory
    res["counts"] = solve.counts
    res["moves"] = solve.solve_moves
    return res


def mess_puzzle(request):
    target = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    mess = Solve.mess_up(target)
    return HttpResponse(json.dumps(mess), content_type="application/json")


def solve_puzzle(request):
    source = json.loads(request.GET.get("source"))
    solve = Solve(source, target)
    result = {}
    solve.DFS_search()
    result["DFS"] = Push(solve)
    solve.A_search()
    result["A*"] = Push(solve)
    solve.BFS_search()
    result["BFS"] = Push(solve)
    solve.B_search()
    result["B*"] = Push(solve)

    #########
    # solve1 = copy.deepcopy(solve)
    # solve1.A_search()
    # result["A*"] = Push(solve1)
    # solve2 = copy.deepcopy(solve)
    # solve2.BFS_search()
    # result["BFS"] = Push(solve2)
    return HttpResponse(json.dumps(result), content_type="application/json")


def show(request):
    return render(request, 'index.html')


def echarts(request):
    return render(request, 'echarts.html')
