# -*- coding: utf-8 -*-
import collections

Post = collections.namedtuple('Post', ['title', 'author', 'image', 'thumb', 'text', 'category', 'date'])

ids = [1, 2, 3, 4, 5]

posts = {
    1: Post(
         u'''Comércio Mundial''',
         u'Fred',
         u'http://agenciatarrafa.com.br/2015/wp-content/uploads/2015/09/google-ads-1000x300.jpg',
         u'http://1un1ba2fg8v82k48vu4by3q7.wpengine.netdna-cdn.com/wp-content/uploads/2014/05/Mobile-Analytics-Picture-e1399568637490-350x227.jpg',
         u'''
         A matéria intitulada Comércio mundial tem o pior ano desde a crise financeira de 2008, divulgada hoje pela Folha de S. Paulo, apresenta 2015 como o pior ano para o comércio mundial desde a crise financeira de 2009. Indicando que boa parte da queda está relacionada à desaceleração registrada pela China e outras economias emergentes.
         O que vemos para o Brasil, que passa por sua pior recessão em mais de um século, é que o desempenho no comércio mundial já apresentava tendência de queda desde 2014. Isso pode ser visto nos dados disponibilizados pelo portal DataViva.info.
         A China se tornou fundamental para o Brasil em suas relações comerciais, o que quer dizer que qualquer desaceleração por lá certamente nos atingirá por aqui. A importações chinesas de produtos brasileiros mostrou uma acentuada queda já em 2014. Revelando que os resultados obtidos em 2015 foram impactados por uma desaceleração que iniciou um ano antes.
         No entanto, o colapso nas importações chinesas de produtos brasileiros ocorreu principalmente pela queda na participação das exportações de Produtos Minerais para aquele país. Em 2013, o Brasil exportou para a China cerca de US$ 53,7 bilhões em produtos minerais. Já em 2014, esse valor chegou a cerda de US$ 49,8 bilhões, representando uma queda de cerca de 9% ainda em 2014.
         São, portanto, inequívocos os problemas de curto e de longo prazo para o Brasil. No curto o maior impacto são os limites da exportação de commodities - restrição de demanda - e os preços desfavoráveis. Entretanto, no longo prazo, com a acomodação da taxa de crescimento da China em patamares normais - muito menores que os vigentes -, o impacto será bem maior, primeiro porque o nosso país não poderá mais contar com o crescimento exponencial do consumo e demanda por commodities, e segundo porque os preços internacionais serão estabelecidos estruturalmente em níveis baixos por conta do aumento expressivo da oferta.
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
         u'Seu Madruga',
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

