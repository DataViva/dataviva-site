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
      u'26/10/2015'),
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
      u'19/01/2016'),
   Article(3,
      u'A MODELAGEM MATEMÁTICA ATRAVÉS DE CONCEITOS CIENTÍFICOS',
      u'Mamtemática',
      u'EINSTEIN, A',
      u'Matemática, Educação, Conceitos Científicos',
      u'''
      Este artigo tem como objetivo apresentar uma proposta que utiliza a modelagem matemática
      para promover uma aprendizagem significativa dos conceitos matemáticos de limite e
      continuidade a partir de conceitos científicos. Para isso, a proposta apóia-se nos princípios
      defendidos pela Educação Matemática, pelos Parâmetros Curriculares Nacionais e pela
      abordagem construtivista de Ausubel. O tema científico escolhido para elaborar as situaçõesproblema,
      e assim, explorar os conceitos matemáticos, foi a Lei de Transformação dos Gases
      de Charles-Gay Lussac. As situações-problema elaboradas propiciam o desenvolvimento de
      capacidades como observação, análise, interpretação e validação de dados. Além disso, é capaz
      de promover um ambiente estimulante de educação científica e tecnológica mobilizando o
      potencial criativo dos estudantes. Dessa forma, acredita-se que a proposta permite ao estudante
      utilizar a modelagem matemática como uma ferramenta para compreender os conceitos
      matemáticos e para resolver problemas de diversas áreas do conhecimento.
      ''',
      u'30/09/2009')
]