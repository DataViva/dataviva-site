# -*- coding: utf-8 -*-


class Question:

    def __init__(self, title, selectors, redirect):
        self.title = title
        self.selectors = selectors
        self.redirect = redirect

    @property
    def serialize(self):
        return {
            "title": self.title,
            "selectors": self.selectors,
            "redirect": self.redirect,
        }


class Session:

    def __init__(self, session_title, title, questions):
        self.session_title = session_title
        self.title = title
        self.questions = questions


development_agents_questions = [
    Question('Qual a rede de produtos da Localidade Y?',
             selectors=["Location"],
             redirect="/location/%s"),

    Question('Quais os produtos mais próximos da estrutura produtiva da Localidade Y?',
             selectors=["Location"],
             redirect="/location/%s"),

    Question('Quais os produtos de maior complexidade exportados por uma Localidade Y?',
             selectors=["Location"],
             redirect="/location/%s"),

    Question('Quais os produtos de maior complexidade importados por uma Localidade Y?',
             selectors=["Location"],
             redirect="/location/%s"),

    Question('Qual a rede de atividades da Localidade Y?',
             selectors=["Location"],
             redirect="/location/%s"),

    Question('Quais as atividades mais próximas da estrutura produtiva da Localidade Y?',
             selectors=["Location"],
             redirect="/location/%s"),

    Question('Quais localidades concentram o emprego na Atividade X?',
             selectors=["Industry"],
             redirect="/industry/%s"),
]

student_questions = [
    Question('Quais os cursos de nível superior oferecidos na Localidade Y?',
             selectors=["Location"],
             redirect="/location/%s"),

    Question('Quais os cursos de nível técnico oferecidos na Localidade Y?',
             selectors=["Location"],
             redirect="/location/%s"),

    Question('Qual o salário médio da Ocupação Z na Localidade Y?',
             selectors=["Occupation", "Location"],
             redirect="/occupation/%s?bra_id=%s"),

    Question('Em quais localidades paga-se o maior salário médio da Ocupação Z?',
             selectors=["Occupation"],
             redirect="/occupation/%s"),

    Question('Em quais localidades cresce o número de empregados da Ocupação Z?',
             selectors=["Occupation"],
             redirect="/occupation/%s"),

    Question('Quais os principais produtos exportados pela Localidade Y?',
             selectors=["Location"],
             redirect="/location/%s"),

    Question('Quais as principais atividades econômicas de uma Localidade Y?',
             selectors=["Location"],
             redirect="/location/%s"),
]

entrepreneur_questions = [
    Question("Qual o número de estabelecimentos na Atividade X, na Localidade Y?",
             selectors=["Industry", "Location"],
             redirect="/industry/%s?bra_id=%s"),

    Question("Qual o salário médio da Atividade X, na Localidade Y?",
             selectors=["Industry", "Location"],
             redirect="/industry/%s?bra_id=%s"),

    Question("Qual o salário médio da Ocupação Z, na Atividade X, na Localidade Y?",
             selectors=["Occupation", "Industry", "Location"],
             redirect="/occupation/%s?cnae_id=%s?bra_id=%s"),

    Question("Quais os principais parceiros comerciais de um Produto P na Localidade Y?",
             selectors=["Product", "Location"],
             redirect="/product/%s?bra_id=%s"),

    Question("Quais localidades concentram o emprego na Atividade X?",
             selectors=["Industry"],
             redirect="/industry/%s"),

    Question("Quais as localidades que mais importam o Produto P?",
             selectors=["Product"],
             redirect="/product/%s"),

    Question("Quais as localidades que mais exportam o Produto P?",
             selectors=["Product"],
             redirect="/product/%s"),

    Question("Quais os produtos mais próximos da estrutura produtiva da Localidade Y?",
             selectors=["Location"],
             redirect="/location/%s"),

    Question("Quais os cursos de nível superior oferecidos na Localidade Y?",
             selectors=["Location"],
             redirect="/location/%s"),

    Question("Quais os cursos de nível técnico oferecidos na Localidade Y?",
             selectors=["Location"],
             redirect="/location/%s"),
]


entrepreneur_session = Session(
    session_title="Empreendedores",
    title="Identifique o perfil econômico e as oportunidades de negócios de uma região",
    questions=entrepreneur_questions
)


development_agents_session = Session(
    session_title="Agentes de Desenvolvimento",
    title="Avalie a criação de políticas de desenvolvimento de acordo com a localidade",
    questions=development_agents_questions
)

student_session = Session(
    session_title="Estudantes e Profissionais",
    title="Descubra informações sobre empregos disponíveis, renda por ocupação e cursos",
    questions=student_questions
)

SESSIONS = {
    'entrepreneur': entrepreneur_session,
    'development_agents': development_agents_session,
    'student': student_session,
}
