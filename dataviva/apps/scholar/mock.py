# -*- coding: utf-8 -*-
import collections

Article = collections.namedtuple('Article', ['id', 'title', 'theme', 'author', 'key_words', 'abstract', 'publication_date'])

articles = [
    Article(1,
         u'A TECNOLOGIA COMO CAMINHO PARA UMA EDUCAÇÃO CIDADÃ',
         u'Tecnologia',
         u'BATISTA, C; SATER, A; ALVARENGA, D',
         u'Tecnologia, Educação, Cidadania',
         u'''
         Este artigo tem como objetivo refletir sobre a relação entre educação, tecnologia e cidadania
         na atualidade visando uma concepção de currículo inserido na lógica hipertextual. A
         proposta do artigo é dialogar com os conceitos desta tríade averiguando quais os conteúdos
         que precisam ficar claros para dar visibilidade e lugar a uma nova prática educativa que
         ajude na constituição de um cidadão capaz de atuar na sociedade em que está inserido. O
         presente trabalho é uma pesquisa bibliográfica. A coleta das informações foi realizada
         através do levantamento e análise de idéias diferentes trazidas por artigos e livros que
         tratam a temática apresentada. Conclui-se constatandoque a tecnologia aliada à educação
         promove a cidadania, poisestimula a produção de saberes, democratiza o acesso a
         informação e ao conhecimento e potencializa a emancipação social.
         ''',
         u'26 de Outubro de 2015'),
    Article(2,
         u'DIREITOS E LIBERDADES DECLARADOS',
         u'Políticas Públicas',
         u'SILVA, T',
         u'Direito, Liberdade, Política',
         u'''
         Todos os seres humanos podem invocar os direitos e as liberdades proclamados na presente Declaração, 
         sem distinção alguma, nomeadamente de raça, cor, sexo, língua, religião, opinião política ou outra, 
         origem nacional ou social, fortuna, nascimento ou outro estatuto. Além disso, não será feita nenhuma 
         distinção fundada no estatuto político, jurídico ou internacional do país ou do território da 
         naturalidade da pessoa, seja esse país ou território independente, sob tutela, autónomo ou sujeito 
         a alguma limitação de soberania.
         ''',
         u'19 de Janeiro de 2016'),
]