# -*- coding: utf-8 -*-
import collections

Post = collections.namedtuple('Post', ['title', 'author', 'image', 'thumb', 'text', 'category', 'date'])

ids = [1, 2, 3, 4, 5]

posts = {
    1: Post(
         u'''Correlation captured.''',
         u'Fred',
         u'http://agenciatarrafa.com.br/2015/wp-content/uploads/2015/09/google-ads-1000x300.jpg',
         u'http://1un1ba2fg8v82k48vu4by3q7.wpengine.netdna-cdn.com/wp-content/uploads/2014/05/Mobile-Analytics-Picture-e1399568637490-350x227.jpg',
         u'''
         Professores, gestores escolares e equipes de secretarias de educação podem participar do programa de formação da Fundação Lemann e Elos Educacional para promover o aprendizado efetivo dos alunos. Os cursos “Gestão para Aprendizagem” e “Gestão de Sala de Aula” estão com inscrições abertas até o dia 19 de novembro. As atividades devem iniciar em março de 2016.
         O curso “Gestão de Sala de Aula” é aberto para professores e gestores escolares e o curso “Gestão para Aprendizagem” é voltado apenas para os gestores das escolas.
         ''',
         u'Tecnologia',
         u'26 de Outubro de 2015'),
    2: Post(
         u'Mestre da mocagem',
         u'Gilmar',
         u'http://placehold.it/1000x300',
         u'http://lumidesign.ca/wp-content/uploads/2013/11/FRAMED-MIRROR-TV4-350x227.jpg',
         u'''
         Professores, gestores escolares e equipes de secretarias de educação podem participar do programa de formação da Fundação Lemann e Elos Educacional para promover o aprendizado efetivo dos alunos. Os cursos “Gestão para Aprendizagem” e “Gestão de Sala de Aula” estão com inscrições abertas até o dia 19 de novembro. As atividades devem iniciar em março de 2016.
         O curso “Gestão de Sala de Aula” é aberto para professores e gestores escolares e o curso “Gestão para Aprendizagem” é voltado apenas para os gestores das escolas.
         ''',
         u'Tecnologia',
         u'26 de Outubro de 2015'),
    3: Post(
         u'Mestre da mocagem',
         u'Victor',
         u'http://placehold.it/1000x300',
         u'http://i-fakt.ru/wp-content/uploads/2013/04/ikota-350x227.jpg',
         u'''
         Professores, gestores escolares e equipes de secretarias de educação podem participar do programa de formação da Fundação Lemann e Elos Educacional para promover o aprendizado efetivo dos alunos. Os cursos “Gestão para Aprendizagem” e “Gestão de Sala de Aula” estão com inscrições abertas até o dia 19 de novembro. As atividades devem iniciar em março de 2016.
         O curso “Gestão de Sala de Aula” é aberto para professores e gestores escolares e o curso “Gestão para Aprendizagem” é voltado apenas para os gestores das escolas.
         ''',
         u'Tecnologia',
         u'26 de Outubro de 2015'),
    4: Post(
         u'Mestre da mocagem',
         u'Seu ',
         u'http://placehold.it/1000x300',
         u'http://www.nidhimam.in/wp-content/uploads/2014/12/free-video-to-jpg-converter_41-1-350x227.jpg',
         u'''
         Professores, gestores escolares e equipes de secretarias de educação podem participar do programa de formação da Fundação Lemann e Elos Educacional para promover o aprendizado efetivo dos alunos. Os cursos “Gestão para Aprendizagem” e “Gestão de Sala de Aula” estão com inscrições abertas até o dia 19 de novembro. As atividades devem iniciar em março de 2016.
         O curso “Gestão de Sala de Aula” é aberto para professores e gestores escolares e o curso “Gestão para Aprendizagem” é voltado apenas para os gestores das escolas.
         ''',
         u'Tecnologia',
         u'26 de Outubro de 2015'),
    5: Post(
         u'Mestre da mocagem',
         u'Victor',
         u'http://placehold.it/1000x300',
         u'http://2uq7lu1k9rrf39yaal2at56hznc.wpengine.netdna-cdn.com/wp-content/uploads/2013/08/sample-slider-ggob-1-350x227.png',
         u'''
         Professores, gestores escolares e equipes de secretarias de educação podem participar do programa de formação da Fundação Lemann e Elos Educacional para promover o aprendizado efetivo dos alunos. Os cursos “Gestão para Aprendizagem” e “Gestão de Sala de Aula” estão com inscrições abertas até o dia 19 de novembro. As atividades devem iniciar em março de 2016.
         O curso “Gestão de Sala de Aula” é aberto para professores e gestores escolares e o curso “Gestão para Aprendizagem” é voltado apenas para os gestores das escolas.
         ''',
         u'Tecnologia',
         u'26 de Outubro de 2015'),
}

