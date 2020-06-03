\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{rapport}[2014/10/08]

\LoadClass[pdftex,12pt,a4paper]{article}
\RequirePackage{etex}
\RequirePackage[a4paper,vdivide={*,22cm,4cm}]{geometry}

\RequirePackage{xcolor}

\RequirePackage{makeidx} % creation d'index
\RequirePackage[english,french]{babel} % style francais
% pas d'espace automatiques avant les signes de ponctuation doubles !
\NoAutoSpaceBeforeFDP

% graphicx avec la bonne option, le chemin des images 
% et les types d'images valides
\RequirePackage[pdftex]{graphicx}
\graphicspath{{pdfs/}{pngs/}{imgs/}}
\DeclareGraphicsExtensions{.pdf,.png,.mps}

% Al�lioration de la gestion des couleurs du pdf
%\pdfpageattr{/Group << /S /Transparency /I true /CS /DeviceRGB>>}

\makeatletter
\newcommand\frontmatter{%
    \cleardoublepage
  %\@mainmatterfalse
  \pagenumbering{roman}}

\newcommand\mainmatter{%
   % \cleardoublepage
 % \@mainmattertrue
  \pagenumbering{arabic}}

\newcommand\backmatter{%
  \if@openright
    \cleardoublepage
  \else
    \clearpage
  \fi
 % \@mainmatterfalse
   }
\makeatother

\RequirePackage{amsmath,amssymb,amsthm,euscript}
% page de garde
\RequirePackage{pageGardeEnsta}

\RequirePackage{microtype} % Micro ajustement des espacements

\RequirePackage{tabularx}
\RequirePackage{eurosym} % pour le symbole euro
\RequirePackage{float}
\RequirePackage{multicol}
\RequirePackage{float}

\RequirePackage{tipa}

\RequirePackage{pgf,tikz}
\usetikzlibrary{automata,shapes,plotmarks,chains,positioning,shadows,arrows,trees,calc}


% aeguill correspond a ea plus les guillemets francais
\RequirePackage{lmodern}
\RequirePackage[T1]{fontenc}
\RequirePackage[latin1]{inputenc} % pour taper les accents directement

\RequirePackage[hyphens]{url}
\urlstyle{same}
\RequirePackage[pdftex,colorlinks,breaklinks,backref=page]{hyperref}
\RequirePackage{caption}


\RequirePackage[acronymlists={glo},toc]{glossaries} % glossaires
\newglossary{glo}{acr1}{acn1}{Glossaire}
%\newglossary{gloen}{acr2}{acn2}{English glossary}


\RequirePackage{longtable,booktabs}

\unitlength 1cm

\def\nbR{\mathbb{R}}
\def\nbN{\mathbb{N}}
\def\nbQ{\mathbb{Q}}
\def\nbZ{\mathbb{Z}}



\theoremstyle{plain}
\newtheorem{theo}{Th�or�me}
\newtheorem{theoreme}{Th�or�me}
\newtheorem{lemme}{Lemme}
\newtheorem{corollaire}{Corollaire}
\newtheorem*{iremarque}{Remarque}
\newtheorem*{iremarques}{Remarques}
\theoremstyle{definition}
\newtheorem{defi}{D�finition}
\theoremstyle{remark}
\newtheorem{exemple}{Exemple}
\newtheorem{exemples}{Exemples}
\newtheorem*{remarque}{Remarque}
\newtheorem*{remarques}{Remarques}
\newtheorem{prop}{Propri�t�}
\newtheorem*{prop*}{Propri�t�s}



\RequirePackage{ifthen}
