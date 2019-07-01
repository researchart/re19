## Licenses
The tools provided with this artifact fall under various different licenses, which we will describe in the following.

### Ultimate ReqAnalyzer
Ultimate ReqAnalyzer consists of many plugins, all of whom are licensed under [LGPLv3](https://www.gnu.org/licenses/lgpl.html) with a custom linking exception. The license files are
  * ``UAutomizer-linux/LICENSE``
  * ``UAutomizer-linux/LICENSE.GPL``
  * ``UAutomizer-linux/LICENSE.GPL.LESSER``.

Ultimate ReqAnalyzer uses the following libraries or dependencies that are compatible with its license.

| Library | License | 
| --- | --- | 
| Eclipse / OSGI | [Eclipse Public License 2.0](https://www.eclipse.org/org/documents/epl-2.0/EPL-2.0.txt) | 
| [log4j](http://logging.apache.org/log4j/) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) (included in jar-file) |
| [Modified JavaCup](https://github.com/ultimate-pa/javacup) | Standard ML of New Jersey [(Original)](http://www2.cs.tum.edu/projects/cup/licence.php) |
| [Apache Batik](http://xmlgraphics.apache.org/batik/) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) (included in all jar-files) |
| [Apache Commons Collections](http://commons.apache.org/collections/) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) (included in all jar-files) |
| [Apache Xerces](http://xerces.apache.org/) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt) (included in all jar-files) |
| [SMTInterpol](https://github.com/ultimate-pa/smtinterpol) | [LGPLv3](https://github.com/ultimate-pa/smtinterpol/blob/master/COPYING.LESSER) |

Ultimate ReqAnalyzer also contains the binaries for the following SMT solvers. 
| Name | License | License file |
| --- | --- | --- |
| [Z3](https://github.com/Z3Prover/z3) | MIT License  [Redistributable](https://www.gnu.org/licenses/license-list.html#Expat) | ``UAutomizer-linux/z3-LICENSE`` |
| [MathSAT](http://mathsat.fbk.eu/) | [Custom](http://mathsat.fbk.eu/download.html) | ``UAutomizer-linux/mathsat-LICENSE`` |
| [CVC4](http://cvc4.cs.stanford.edu/web/) | Custom | ``UAutomizer-linux/cvc4-LICENSE`` |


### req2ta2UPPAAL
req2ta2UPPAAL consists of two tools, req2ta and UPPAAL.
req2ta is licensed under [LGPLv2](https://www.gnu.org/licenses/lgpl.html). 

UPPAAL uses a custom license. In order to use it, you have to agree to the license by completing an [online form](http://www.it.uu.se/research/group/darts/uppaal/download/registration.php?id=0&subid=10).

The license reads:

> License Agreement
> UPPAAL Release Version
> Please read the license agreement carefully, fill in the form, and press the "Register and Download" button. The information will be sent to the Uppaal team and used for the purpose of registration only.
>
> Copyright (c) 1995-2011 by Uppsala University and Aalborg University.
>
> We (the licensee) understand that Uppaal includes the programs: uppaal.jar, uppaal, uppaal.bat, server, socketserver, and verifyta and that they are supplied "as is", without expressed or implied warranty. We agree on the following:
>
> You (the licensers) do not have any obligation to provide any maintenance or consulting help with respect to Uppaal.
> You neither have any responsibility for the correctness of systems verified using Uppaal, nor for the correctness of Uppaal itself.
> We will never distribute or modify any part of the Uppaal code (i.e. the source code and the object code) without a written permission of Wang Yi (Uppsala University) or Kim G Larsen (Aalborg University).
> We will make only academic use of Uppaal. We understand that academic work means work performed by researchers or students at institutions delivering academic degrees. In addition, the work or the worker may not be contracted by any non-academic institution. Any use at companies, private use, use at national research agencies, or any other non-academic use requires a license of Uppaal.
> Uppaal nor any part of its code may be used or modified for any commercial software product.
> In the event that you should release new versions of Uppaal to us, we agree that they will also fall under all of these terms.


### benchexec
The artifact also contains a binary version of benchexec together with a small extension to support req2ta2UPPAAL.
The extension consists of the file ``benchexec/benchexec/tools/req2ta2UPPAAL.py``.

benchexec is released under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt).
The license file is ``benchexec/LICENSE``. 