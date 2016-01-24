# -*- coding: utf-8 -*-

ATIVIDADE_ECON_STEP = {
    "title": "Selecione uma atividade econômica",
    "label": "por atividade_econ",
    "options": {},
}

OCUPACAO_STEP = {
    "title": "Selecione uma ocupacão",
    "label": "por ocupacao",
    "options": {},
}

MUNICIPIO_STEP = {
    "title": "Selecione um município",
    "label": "por municipio",
    "options": {},
}

PRODUTO_STEP = {
    "title": "Selecione um produto",
    "label": "por produto",
    "options": {},
}

DESTINO_STEP = {
    "title": "Selecione um destino de exportacões",
    "label": "por destino",
    "options": {},
}

ORIGEM_STEP = {
    "title": "Selecione uma origem de importacões",
    "label": "por origem",
    "options": {},
}

LOCATIONS_STEP = {
    "title": "Selecione uma localidade",
    "label": "por locations",
    "options": {},
}


# INTERNATIONAL TRADING
BALANCA_COMERCIAL_STEP = {
    "title": "Visualize a Balanca Comecial",
    "label": "por balanca_comercial",
    "options": {},
}

EXPORTACOES_STEP = {
    "title": "Qual aspecto das exportacões deseja analisar?",
    "label": "por exportacoes",
    "options": {
        "PRODUTO_STEP": PRODUTO_STEP,
        "MUNICIPIO_STEP": MUNICIPIO_STEP,
        "DESTINO_STEP": DESTINO_STEP,
    },
}

IMPORTACOES_STEP = {
    "title": "Qual aspecto das importacões deseja analisar?",
    "label": "por importacoes",
    "options": {
        "PRODUTO_STEP": PRODUTO_STEP,
        "MUNICIPIO_STEP": MUNICIPIO_STEP,
        "ORIGEM_STEP": ORIGEM_STEP,
    },
}

COM_INTERNACIONAL_STEP = {
    "title": "Qual aspecto de Comercio Internacional deseja analisar?",
    "label": "por com_internacional",
    "options": {
        "BALANCA_COMERCIAL_STEP": BALANCA_COMERCIAL_STEP,
        "EXPORTACOES_STEP": EXPORTACOES_STEP,
        "IMPORTACOES_STEP": IMPORTACOES_STEP
    },
}


# EMPLOYMENT & SALARY
MASSA_SALARIAL_STEP = {
    "title": "Visualize a Balanca Comecial",
    "label": "por massa_salarial",
    "options": {
        "ATIVIDADE_ECON_STEP": ATIVIDADE_ECON_STEP,
        "OCUPACAO_STEP": OCUPACAO_STEP,
        "MUNICIPIO_STEP": MUNICIPIO_STEP,
    },
}

EMPREGOS_STEP = {
    "title": "Selecione qual aspecto deseja analisar",
    "label": "por empregos",
    "options": {
        "ATIVIDADE_ECON_STEP": ATIVIDADE_ECON_STEP,
        "OCUPACAO_STEP": OCUPACAO_STEP,
        "MUNICIPIO_STEP": MUNICIPIO_STEP
    },
}

SAL_EMP_STEP = {
    "title": "Qual aspecto de Salários e Empregos deseja analisar?",
    "label": "por sal_emp",
    "options": {
        "MASSA_SALARIAL_STEP": MASSA_SALARIAL_STEP,
        "EMPREGOS_STEP": EMPREGOS_STEP},
}


WIZARD_LOCATIONS = {
    "title": "Qual localidade deseja analisar?",
    "label": "por wizard",
    "main_dimension": LOCATIONS_STEP,
    "options": {
        "COM_INTERNACIONAL_STEP": COM_INTERNACIONAL_STEP,
        "SAL_EMP_STEP": SAL_EMP_STEP
    },
}

WizTree = {
    "locations": WIZARD_LOCATIONS,
}


def get_next_step(wiz, answers):

    print wiz["title"]
    print "###################"

    options = wiz["options"]
    print get_step_options(wiz)
    for op_key, op_value in options.items():
        for ans in answers:
            if op_key == ans[0]:

                print ">>>>>>>>"
                print ans
                print ">>>>>>>>"

                return get_next_step(op_value, answers)  # recursion, yay!
    return wiz


def get_step_options(wstep):
    opts = []
    for k, v in wstep["options"].items():
        opts.append((k, v["label"],))
    return opts

if __name__ == '__main__':
    import json

    wiz = WizTree["locations"]
    prev = [
        ("COM_INTERNACIONAL_STEP", True,),
        ("EXPORTACOES_STEP", True,),
    ]

    print json.dumps({
        "session_name": "locations",
        "current_answer": ("PRODUTO_STEP", True,),
        "previous_answers": prev,
    })

    wstep = get_next_step(wiz, prev)
    print get_step_options(wstep)
